import re
import cv2
import math

import numpy as np
import pytesseract
from PIL import Image
from fuzzywuzzy import fuzz
from datetime import datetime
from typing import Any, Callable
from pyzbar.pyzbar import decode
from deskew import determine_skew
from collections import defaultdict

import ipih
from pih_tls import Logger
from pih import A, NotFound
from pih.collections import (
    Rect,
    Result,
    PolibasePerson,
    BarcodeInformation,
    DocumentDescription,
    MedicalResearchType,
    ChillerIndicationsValue,
    PolibaseDocumentDescription,
)
from pih.consts import CHARSETS
from RecognizeService.const import *
from RecognizeService.collection import *
from pih.tools import ne, e, js, j, one, escs


class ImagePreprocessing:
    @staticmethod
    def magic(image_array: np.ndarray) -> np.ndarray:
        return cv2.GaussianBlur(
            ImagePreprocessing.for_backgrounded_text_open_morphology(
                ImagePreprocessing.for_backgrounded_text_v0(image_array, 60), 1, 3
            ),
            (3, 3),
            0,
        )

    @staticmethod
    def global_threshold(image_array: np.ndarray, blur_value: int = 5) -> np.ndarray:
        return cv2.threshold(
            cv2.medianBlur(cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY), blur_value),
            127,
            255,
            cv2.THRESH_BINARY,
        )[1]

    @staticmethod
    def preprocess(image_array: np.ndarray):
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)
        blurred = cv2.blur(gradient, (3, 3))
        _, thresh = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
        thresh = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        return thresh

    @staticmethod
    def adaptive_threshold_v1(image_array: np.ndarray, blur_value: int = 5) -> None:
        return cv2.threshold(
            cv2.GaussianBlur(
                cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
                if len(image_array.shape) > 2
                else image_array,
                (blur_value, blur_value),
                0,
            ),
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )[1]

    @staticmethod
    def for_barcode_detection(image_array: np.ndarray, size: int = 5) -> None:
        return ImagePreprocessing.magic(image_array)

    @staticmethod
    def adaptive_threshold_v2(
        image_array: np.ndarray, blur_value: int = 3
    ) -> np.ndarray:
        return cv2.threshold(
            cv2.GaussianBlur(image_array, (blur_value, blur_value), 0),
            127,
            255,
            cv2.THRESH_TOZERO,
        )[1]

    @staticmethod
    def blackhat_morphology(
        image_array: np.ndarray, kerenel_size: int = 3, size: tuple[int, int] = (25, 7)
    ) -> np.ndarray:
        return 255 - cv2.morphologyEx(
            cv2.GaussianBlur(image_array, (kerenel_size, kerenel_size), 0),
            cv2.MORPH_BLACKHAT,
            cv2.getStructuringElement(cv2.MORPH_RECT, size),
        )

    @staticmethod
    def for_mrz_v1(image_array: np.ndarray, blur_value: int = 3) -> np.ndarray:
        return ImagePreprocessing.adaptive_threshold_v2(image_array, blur_value)

    @staticmethod
    def for_mrz_v2(
        image_array: np.ndarray, kerenel_size: int = 3, size: tuple[int, int] = (25, 7)
    ) -> np.ndarray:
        return ImagePreprocessing.blackhat_morphology(image_array, kerenel_size, size)

    @staticmethod
    def for_backgrounded_text_v1(
        image_array: np.ndarray, threshBias: float = 0.2, minArea: int = 5
    ) -> None:
        def area_filter(binary_image, minArea):
            (
                totalComponents,
                labeledPixels,
                componentsStats,
                _,
            ) = cv2.connectedComponentsWithStats(binary_image, connectivity=4)
            remaining_comp_labels = [
                i for i in range(1, totalComponents) if componentsStats[i][4] >= minArea
            ]
            outImage = np.where(
                np.isin(labeledPixels, remaining_comp_labels) == True, 255, 0
            ).astype(np.uint8)
            return outImage

        imgFloat = image_array.astype(float) / 255.0
        kChannel = 1 - np.max(imgFloat, axis=1)
        kChannel = (255 * kChannel).astype(np.uint8)
        autoThresh, binaryImage = cv2.threshold(
            kChannel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        autoThresh = threshBias * autoThresh
        _, binaryImage = cv2.threshold(kChannel, autoThresh, 255, cv2.THRESH_BINARY)
        binaryImage = area_filter(binaryImage, minArea)
        binaryImage = 255 - binaryImage
        return binaryImage

    @staticmethod
    def for_ocr(
        image_array: np.ndarray,
        binary_threshold: int | None = 120,
        minArea: int = 5,
        dilation_kernel: int | None = None,
        dilation_iterations: int = 1,
        morphology_close_kernel: int | None = None,
        morphology_close_iterations: int = 2,
    ) -> np.ndarray:
        if e(binary_threshold):
            binary_image = cv2.threshold(
                cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY),
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU,
            )[1]
        else:

            def areaFilter(minArea, inputImage):
                (
                    componentsNumber,
                    labeledImage,
                    componentStats,
                    _,
                ) = cv2.connectedComponentsWithStats(inputImage, connectivity=4)
                remainingComponentLabels = [
                    i
                    for i in range(1, componentsNumber)
                    if componentStats[i][4] >= minArea
                ]
                return np.where(
                    np.isin(labeledImage, remainingComponentLabels) == True, 255, 0
                ).astype("uint8")

            imgFloat = image_array.astype(float) / 255.0
            kChannel = 1 - np.max(imgFloat, axis=2)
            kChannel = (255 * kChannel).astype(np.uint8)
            _, binary_image = cv2.threshold(
                kChannel, binary_threshold, 255, cv2.THRESH_BINARY
            )
            binary_image = areaFilter(minArea, binary_image)
        if ne(dilation_kernel):
            binary_image = cv2.dilate(
                binary_image,
                np.ones((dilation_kernel, dilation_kernel), np.uint8),
                iterations=dilation_iterations,
            )
        if ne(morphology_close_kernel):
            morphology_kernel = cv2.getStructuringElement(
                cv2.MORPH_RECT, (morphology_close_kernel, morphology_close_kernel)
            )
            binary_image = cv2.bitwise_not(
                cv2.morphologyEx(
                    binary_image,
                    cv2.MORPH_CLOSE,
                    morphology_kernel,
                    iterations=morphology_close_iterations,
                    borderType=cv2.BORDER_REFLECT101,
                )
            )
        return cv2.bitwise_not(binary_image)

    @staticmethod
    def for_backgrounded_text_close_morphology(
        image_array: np.ndarray, size: int = 3, iterations: int = 1
    ) -> Any:
        return cv2.morphologyEx(
            image_array,
            cv2.MORPH_CLOSE,
            np.ones((size, size), np.uint8),
            iterations=iterations,
        )

    @staticmethod
    def for_backgrounded_text_open_morphology(
        image_array: np.ndarray, size: int = 3, iterations: int = 1
    ) -> Any:
        return cv2.morphologyEx(
            image_array,
            cv2.MORPH_OPEN,
            np.ones((size, size), np.uint8),
            iterations=iterations,
        )

    def for_backgrounded_text_open_area(
        image_array: np.ndarray, min_size: int = 10
    ) -> Any:
        nb_blobs, im_with_separated_blobs, stats, _ = cv2.connectedComponentsWithStats(
            image_array
        )
        sizes = stats[:, -1]
        sizes = sizes[1:]
        nb_blobs -= 1
        im_result = np.zeros_like(im_with_separated_blobs)
        for blob in range(nb_blobs):
            if sizes[blob] >= min_size:
                im_result[im_with_separated_blobs == blob + 1] = 0
        return im_result

    @staticmethod
    def for_backgrounded_text_v0(image_array: np.ndarray, radius: int = 80) -> Any:
        def process(im, r: int):
            med = cv2.medianBlur(im, 2 * radius + 1)
            with np.errstate(divide="ignore", invalid="ignore"):
                normalized = np.where(
                    med <= 1, 1, im.astype(np.float32) / med.astype(np.float32)
                )
            return (normalized, med)

        normalized = process(cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY), radius)[0]
        return cv2.threshold(
            (normalized.clip(0, 1) * 255).astype("u1"),
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )[1]


class RecognizeApi:
    def recognize_display(self, indications_value: ChillerIndicationsValue) -> None:
        image_path: str = A.PTH_IND.CHILLER_DATA_IMAGE_LAST
        source_image_array: np.ndarray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        main_image_array: np.ndarray | None = None
        left_image_array: np.ndarray | None = None
        bottom_image_array: np.ndarray | None = None
        right_image_array: np.ndarray | None = None
        cropped_image_array: np.ndarray | None = None
        padding: int = 0
        flag_area_size: int = 0
        image_array_for_contours_detection: np.ndarray = cv2.erode(
            source_image_array, None, iterations=2
        )
        image_array_for_contours_detection = cv2.dilate(
            image_array_for_contours_detection, None, iterations=4
        )
        _, image_array_for_contours_detection = cv2.threshold(
            image_array_for_contours_detection, 128, 255, cv2.THRESH_BINARY
        )
        image_array_for_contours_detection = cv2.Canny(
            cv2.bilateralFilter(image_array_for_contours_detection, 11, 17, 17), 30, 200
        )
        self.logger.write_image("edged", image_array_for_contours_detection)
        contours = cv2.findContours(
            image_array_for_contours_detection,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )[0]
        image_width, image_height = source_image_array.shape
        display_contours: list[int] = [image_width, image_height, 0, 0]
        if e(contours):
            indications_value.indicators = A.CT_I.CHILLER.INDICATOR_EMPTY_DISPLAY
            return
        else:
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                display_contours[0] = min(x, display_contours[0])
                display_contours[1] = min(y, display_contours[1])
                display_contours[2] = max(x + w, display_contours[2])
                display_contours[3] = max(y + h, display_contours[3])
        padding = int(image_height / 90)
        display_contours[0] -= padding
        display_contours[1] -= padding
        display_contours[2] += padding
        display_contours[3] += padding
        image_height = display_contours[3] - display_contours[1]
        image_width = int(image_height * 2.465)
        cropped_image_array: np.ndarray = source_image_array[
            display_contours[1] : display_contours[3],
            display_contours[0] : display_contours[0] + image_width,
        ]
        self.logger.write_image("cropped", cropped_image_array)
        cv2.imwrite(
            A.PTH.INDICATIONS.CHILLER_DATA_IMAGE_LAST_RESULT, cropped_image_array
        )
        flag_area_size: int = int(image_height * 0.31)
        main_image_array: np.ndarray = cropped_image_array[
            0 : image_height - flag_area_size,
            flag_area_size + padding : image_width - flag_area_size,
        ]
        edged_image_array_cropped = image_array_for_contours_detection[
            display_contours[1] : display_contours[3],
            display_contours[0] : display_contours[0] + image_width,
        ]
        left_image_array = edged_image_array_cropped[
            0:image_height, 0 : flag_area_size + padding
        ]
        bottom_image_array = edged_image_array_cropped[
            image_height - flag_area_size : image_height,
            flag_area_size : image_width - flag_area_size,
        ]
        contours = cv2.findContours(
            bottom_image_array.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )[0]
        flag_min_height: int = int(image_height * 0.2)
        bottom_image_width: int = image_width - 2 * flag_area_size
        flag_area_width: int = bottom_image_width / 6
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if h > flag_min_height:
                flag_index: int = round(x / flag_area_width)
                indications_value.indicators += pow(2, flag_index)
        right_image_array: np.ndarray = edged_image_array_cropped[
            0:image_height, image_width - flag_area_size : image_width
        ]
        self.logger.write_image("main", main_image_array)
        prepeared_image_array: np.ndarray = main_image_array
        prepeared_image_array = cv2.threshold(
            prepeared_image_array, 127, 255, cv2.THRESH_BINARY
        )[1]
        image_width, image_height = prepeared_image_array.shape
        prepeared_image_array = cv2.warpPerspective(
            prepeared_image_array,
            np.float32([[1, 0.13, 0], [0, 1, 0], [0, 0, 1]]),
            (image_height, image_width),
        )
        prepeared_image_array = cv2.morphologyEx(
            prepeared_image_array,
            cv2.MORPH_CLOSE,
            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 12)),
        )
        prepeared_image_array = 255 - prepeared_image_array
        prepeared_image_array = cv2.copyMakeBorder(
            prepeared_image_array,
            padding * 2,
            padding * 2,
            padding * 2,
            padding * 2,
            cv2.BORDER_CONSTANT,
            value=[255, 255, 255],
        )
        temperature_value: str = RecognizeApi.image_to_string(
            Image.fromarray(prepeared_image_array).convert("RGB"),
            language="ssd",
            char_whitelist=".1234567890HP",
        )
        temperature_value = temperature_value.replace(" ", "")
        temperature: float = 0
        for item in temperature_value.splitlines():
            try:
                temperature = float(item)
                if temperature > 100:
                    temperature = temperature / 10
            except ValueError as error:
                pass
        indications_value.temperature = temperature
        self.logger.write_image(
            f"{indications_value.temperature}\nИндикаторы: {indications_value.indicators}",
            prepeared_image_array,
        )

        if self.logger.level > 1:
            self.logger.write_image("left", left_image_array)
            self.logger.write_image("right", right_image_array)
            self.logger.write_image("bottom", bottom_image_array)

    STANDART_RATIO: int = 70
    PSM_LIST: list[int] = [6, 1, 3, 4, 11, 12]

    @staticmethod
    def td3_name_convert(value: str) -> str:
        for symbol in RecognizeApi.TD3_SYMBOL_CONVERT_TABLE:
            value = value.replace(symbol, RecognizeApi.TD3_SYMBOL_CONVERT_TABLE[symbol])
        return value

    TD3_SYMBOL_CONVERT_TABLE: dict[str, str] = {
        "3": "ч",
        "4": "ш",
        "9": "ь",
        "7": "ю",
        "8": "я",
    }

    @staticmethod
    def convert_to_mm(value: int) -> float:
        return round(value / 7.81, 2)

    @staticmethod
    def convert_to_px(value: int) -> float:
        return round(value * 7.81, 2)

    @staticmethod
    def crop(image_array: np.ndarray, rect: tuple[int, int, int, int]) -> np.ndarray:
        return image_array[int(rect[1]) : int(rect[3]), int(rect[0]) : int(rect[2])]

    @staticmethod
    def get_text_ratio(
        value1: str, value2: str, type: str = "partial_token_sort_ratio"
    ) -> int:
        function: Callable[[str, str], int] | None = None
        if type == "wr":
            function = fuzz.WRatio
        elif type == "set":
            function = fuzz.token_set_ratio
        elif type == "sort":
            function = fuzz.token_sort_ratio
        else:
            function = fuzz.partial_token_sort_ratio
        return (
            100
            if value1.lower().find(value2.lower()) != -1
            else function(value1, value2)
        )

    @staticmethod
    def image_to_string(
        image: Image.Image | np.ndarray,
        checker: Callable[[str], bool] | None = None,
        language: str | None = None,
        char_whitelist: str | None = None,
        psm: int | None = None,
    ) -> str:
        def action(psm: int) -> str:
            return pytesseract.image_to_string(
                image,
                lang=language or "rus",
                config=js(
                    (
                        js(("--psm", psm)),
                        "--oem 3",
                        (
                            ""
                            if e(char_whitelist)
                            else j(
                                ("-c tessedit_char_whitelist=", escs(char_whitelist))
                            )
                        ),
                    )
                )
            )

        result: str | None = None
        psm_present: bool = ne(psm)
        if psm_present:
            checker = None
        for psm_item in [psm] if psm_present else RecognizeApi.PSM_LIST:
            if e(checker):
                result = action(psm_item)
                break
            else:
                local_result: str | None = action(psm_item)
                if checker(local_result):
                    result = local_result
                    break
        return result

    @staticmethod
    def rotate(image_array: np.ndarray, angle: float) -> np.ndarray:
        old_width, old_height = image_array.shape[:2]
        angle_radian = math.radians(angle)
        width = abs(np.sin(angle_radian) * old_height) + abs(
            np.cos(angle_radian) * old_width
        )
        height = abs(np.sin(angle_radian) * old_width) + abs(
            np.cos(angle_radian) * old_height
        )
        image_center = tuple(np.array(image_array.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        rot_mat[1, 2] += (width - old_width) / 2
        rot_mat[0, 2] += (height - old_height) / 2
        return cv2.warpAffine(
            image_array,
            rot_mat,
            (int(round(height)), int(round(width))),
            borderValue=(0, 0, 0),
        )

    @staticmethod
    def get_element_container_with_max_ratio(list: list[tuple[Any, int]]) -> Any | None:
        return (
            None if e(list) else sorted(list, key=lambda item: item[1], reverse=True)[0]
        )

    def get_polibase_document(self, title: str) -> A.CT_P_DT | None:
        comparing_result: list[tuple[A.CT_P_DT, int]] = []
        document_description: PolibaseDocumentDescription | None = None
        polibase_document: A.CT_P_DT | None = None
        for polibase_document in A.CT_P_DT.sorted():
            document_description = A.D.get(polibase_document)
            ratio: int = RecognizeApi.get_text_ratio(
                document_description.title, title, "set"
            )
            if ratio >= document_description.threshold:
                comparing_result.append((polibase_document, ratio))
        if e(comparing_result):
            return None
        return RecognizeApi.get_element_container_with_max_ratio(comparing_result)[0]

    @staticmethod
    def get_max_horizotal_line(
        image_array: np.ndarray, image_height: int
    ) -> tuple[tuple[int, int, int, None], list[Any], Any] | None:
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        detect_horizontal = cv2.morphologyEx(
            thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
        )
        countur_list = cv2.findContours(
            detect_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        countur_list = countur_list[0] if len(countur_list) == 2 else countur_list[1]
        result_line_list: Any = None
        line_group_collection: dict[int, list[tuple[int, int, int, int]]] = defaultdict(
            list
        )
        group_index: int = 0
        last_y: int | None = None
        left: int | None = None
        right: int | None = None
        bounding_map: dict[int, dict[int, tuple[int, int, int, int]]] = defaultdict(
            dict
        )
        for countur in countur_list:
            x, y, w, h = cv2.boundingRect(countur)
            if y > image_height * 0.1 and y < image_height * 0.9:
                bounding_map[x][y] = (x, y, w, h)
                if e(last_y):
                    last_y = y
                else:
                    if abs(last_y - y) > 10:
                        group_index += 1
                    last_y = y
                line_group_collection[group_index].append(bounding_map[x][y])
                if e(left):
                    left = x
                else:
                    left = min([left, x])
                if e(right):
                    right = x + w
                else:
                    right = max([right, x + w])
        result_line_list_collection: list[tuple(int, list[Any])] = []

        def get_x(item) -> int:
            return bounding_map[item[0]][item[1]][0]

        for group_index in line_group_collection:
            group_line_list: list = sorted(
                line_group_collection[group_index], key=get_x
            )
            min_rect: Any = group_line_list[0]
            max_rect: Any = group_line_list[-1]
            result_line_list_collection.append(
                (max_rect[0] - min_rect[0] + max_rect[2], group_line_list)
            )
        if e(result_line_list_collection):
            return None
        result_line_list = sorted(
            result_line_list_collection, key=lambda item: item[0], reverse=True
        )[0]
        return (left, result_line_list[1][0][1], right - left, None), result_line_list[
            1
        ]
    
    

    def extruct_barcode_information_from_image(
        self, value: Image.Image, make_preprocess: bool = True
    ) -> list[BarcodeInformation]:
        image_array: np.ndarray = np.array(value)
        if make_preprocess:
            image_array = ImagePreprocessing.for_barcode_detection(image_array)
        self.logger.write_image("Изображение для распознавания штрих-кода", value)
        symbols: list[int] = A.D.map(lambda item: A.D_Ex.decimal(item), A.CT_P.BARCODE.SUPPORT_FORMATS)
        barcode_list = decode(image_array, symbols)
        result: list[tuple[str, str, Rect]] = []
        if ne(barcode_list):
            for barcode in barcode_list:
                if ne(barcode.data):
                    result.append(
                        BarcodeInformation(
                            barcode.data.decode(CHARSETS.UTF8),
                            str(barcode.type).lower(),
                            barcode.rect,
                        )
                    )
        return result

    @staticmethod
    def deskew(image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(
            image,
            matrix,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE,
        )

    @staticmethod
    def date_correction(value: str) -> str:
        for item in CORRECTION_TABLE["date"]:
            for symbol in item[1]:
                value = value.replace(symbol, item[0])
        return value

    @property
    def tesseract_psm(self) -> int:
        return RecognizeApi.PSM_LIST[0]

    def __init__(self, logger: Logger):
        self.result: RecognizeResult | None = None
        self.polibase_document_recognize_result: PolibaseDocumentRecognizeResult | None = (
            None
        )
        self.medical_direction_document_recognize_holder: MedicalDirectionDocumentRecognizeResultHolder | None = (
            None
        )
        self.config: RecognizeConfig | None = None
        self.logger = logger

    def read_medical_direction_number_and_date(self, line: str) -> bool:
        def check() -> bool:
            return ne(
                self.medical_direction_document_recognize_holder.recognize_result.number
            )

        if not check():
            ratio: int = fuzz.partial_token_set_ratio(
                line, MedicalDirectionDocumentDescriptor.TITLE
            )
            if ratio >= RecognizeApi.STANDART_RATIO:
                list: list[str] = A.D.split_with_not_empty_items(line)
                for item in list:
                    if not check():
                        value: int | None = A.D_Ex.decimal(item)
                        if ne(value):
                            self.medical_direction_document_recognize_holder.recognize_result.number = (
                                value
                            )
                    elif e(
                        self.medical_direction_document_recognize_holder.recognize_result.date
                    ):
                        if (
                            self.medical_direction_document_recognize_holder.modification
                            != MedicalDirectionDocumentDescriptor.MODIFICATIONS.MODE_1
                        ):
                            value: datetime | None = A.D_Ex.datetime(
                                item, A.CT.DATE_FORMAT
                            )
                            if ne(value):
                                self.medical_direction_document_recognize_holder.recognize_result.date = (
                                    value
                                )
                                return True
                        else:
                            return True
                return check()
            else:
                return None

    def read_person_ensurence_number(self, line: str) -> bool | None:
        def check() -> bool:
            return ne(
                self.medical_direction_document_recognize_holder.recognize_result.person_ensurence_number
            )

        if not check():
            ratio: int = fuzz.WRatio(
                line,
                MedicalDirectionDocumentDescriptor.get_person_polis_title(
                    self.medical_direction_document_recognize_holder.modification
                ),
            )
            if ratio >= RecognizeApi.STANDART_RATIO:
                list: list[str] = A.D.split_with_not_empty_items(line)
                for index, item in enumerate(list):
                    if (
                        fuzz.WRatio(
                            item,
                            MedicalDirectionDocumentDescriptor.get_person_polis_title(
                                self.medical_direction_document_recognize_holder.modification
                            ).split(" ")[-1],
                        )
                        >= RecognizeApi.STANDART_RATIO
                    ):
                        break
                for item in list[index + 1 :]:
                    if not check():
                        value: str = A.D_Ex.decimal(item)
                        if ne(value):
                            self.medical_direction_document_recognize_holder.recognize_result.person_ensurence_number = (
                                value
                            )
                            index += 1
                    else:
                        if (
                            self.medical_direction_document_recognize_holder.modification
                            == MedicalDirectionDocumentDescriptor.MODIFICATIONS.NORMAL
                        ):
                            self.medical_direction_document_recognize_holder.recognize_result.person_ensurence_agent = " ".join(
                                list[index + 1 :]
                            )
                        return True
                return check()
            else:
                return None

    def read_person_name(self, line: str) -> bool | None:
        if e(self.result.person_name):
            ratio: int = fuzz.WRatio(
                line,
                MedicalDirectionDocumentDescriptor.get_person_name_title(
                    self.medical_direction_document_recognize_holder.modification
                ),
            )
            if ratio >= RecognizeApi.STANDART_RATIO:
                list: list[str] = A.D.split_with_not_empty_items(line)
                for index, item in enumerate(list):
                    if (
                        fuzz.WRatio(
                            item,
                            MedicalDirectionDocumentDescriptor.get_person_name_title(
                                self.medical_direction_document_recognize_holder.modification
                            ).split(" ")[-1],
                        )
                        >= RecognizeApi.STANDART_RATIO
                    ):
                        self.result.person_name = " ".join(list[index + 1 :])
                        self.result.person_name = self.result.person_name.lower()
                        self.result.person_name = A.D_F.name(
                            self.result.person_name, True, 3
                        ).strip()
                        return True
            else:
                return None

    def read_person_birthday(self, line: str) -> bool | None:
        if e(
            self.medical_direction_document_recognize_holder.recognize_result.person_birthday
        ):
            ratio: int = fuzz.WRatio(
                line,
                MedicalDirectionDocumentDescriptor.get_birthday_title(
                    self.medical_direction_document_recognize_holder.modification
                ),
            )
            if ratio >= RecognizeApi.STANDART_RATIO:
                list: list[str] = A.D.split_with_not_empty_items(line)
                for index, line_part_item in enumerate(list):
                    if (
                        fuzz.WRatio(
                            line_part_item,
                            MedicalDirectionDocumentDescriptor.get_birthday_title(
                                self.medical_direction_document_recognize_holder.modification
                            ).split(" ")[-1],
                        )
                        >= RecognizeApi.STANDART_RATIO
                    ):
                        index += 1
                        break
                for line_part_item in list[index:]:
                    value: datetime | None = A.D_Ex.datetime(
                        RecognizeApi.date_correction(line_part_item), A.CT.DATE_FORMAT
                    )
                    if ne(value):
                        self.medical_direction_document_recognize_holder.recognize_result.person_birthday = (
                            value
                        )
                        return True
            else:
                return None

    def read_medical_research_type(self, line: str) -> bool | None:
        def check() -> bool:
            return ne(
                self.medical_direction_document_recognize_holder.recognize_result.research_code
            )

        if self.medical_direction_document_recognize_holder.type_line_found:
            if not check():
                self.medical_direction_document_recognize_holder.type_line_list.append(
                    line
                )
                medical_direction_type: MedicalResearchType
                for medical_direction_type in A.CT_MRT:
                    ratio: int = RecognizeApi.get_text_ratio(
                        line, A.D.get(medical_direction_type).title_list[0]
                    )
                    if ratio >= RecognizeApi.STANDART_RATIO:
                        self.medical_direction_document_recognize_holder.type_ratio_list.append(
                            (medical_direction_type.name, ratio, line)
                        )
                    if ratio == 100:
                        break
                medical_direction_type_container: Any | None = (
                    RecognizeApi.get_element_container_with_max_ratio(
                        self.medical_direction_document_recognize_holder.type_ratio_list
                    )
                )
                if ne(medical_direction_type_container):
                    self.medical_direction_document_recognize_holder.recognize_result.research_type = medical_direction_type_container[
                        0
                    ]
                    medical_direction_type_code_string: str = (
                        medical_direction_type_container[2]
                    )
                    self.medical_direction_document_recognize_holder.recognize_result.research_code = one(
                        re.findall(
                            "[А\\.\\d]+",
                            medical_direction_type_code_string[
                                0 : medical_direction_type_code_string.find(
                                    A.D.get(
                                        A.D.get(
                                            A.CT_MRT,
                                            self.medical_direction_document_recognize_holder.recognize_result.research_type,
                                        )
                                    ).title_list[0]
                                )
                            ],
                        )
                    )
            return check()
        else:
            ratio: int = RecognizeApi.get_text_ratio(
                line,
                MedicalDirectionDocumentDescriptor.get_medical_direction_type_title(
                    self.medical_direction_document_recognize_holder.modification
                ),
                "set",
            )
            self.medical_direction_document_recognize_holder.type_line_found = (
                ratio >= RecognizeApi.STANDART_RATIO
            )

    def read_ogrn(self, text: str) -> None:
        if (
            RecognizeApi.get_text_ratio(
                text, MedicalDirectionDocumentDescriptor.OGRN_TITLE, "sort"
            )
            >= RecognizeApi.STANDART_RATIO
        ):
            ogrn_list: list[str] = A.D.split_with_not_empty_items(text)
            for index, item in enumerate(ogrn_list):
                if (
                    RecognizeApi.get_text_ratio(
                        item,
                        MedicalDirectionDocumentDescriptor.OGRN_TITLE.split(" ")[-1],
                        "sort",
                    )
                    >= RecognizeApi.STANDART_RATIO
                ):
                    index += 1
                    break
            for item in ogrn_list[index:]:
                value: int | None = A.D_Ex.decimal(item)
                if ne(value):
                    self.medical_direction_document_recognize_holder.recognize_result.ogrn_number = (
                        value
                    )
                    break

    def find_polibase_person(self) -> None:
        try:
            polibase_person_list_filtered_result: Result[
                list[PolibasePerson]
            ] | None = None
            polibase_person_list_result: Result[
                list[PolibasePerson]
            ] | None = A.R_P.persons_by_name(self.result.person_name)
            if (
                not A.R.is_empty(polibase_person_list_result)
                and len(polibase_person_list_result.data) > 1
            ):

                def filter_function(value: PolibasePerson) -> bool:
                    if self.result.type == A.CT_DT.MEDICAL_DIRECTION:
                        return (
                            self.medical_direction_document_recognize_holder.recognize_result.person_birthday
                            == A.D.datetime_from_string(value.Birth)
                        )

                polibase_person_list_filtered_result = A.R.filter(
                    polibase_person_list_result, filter_function
                )
            self.result.polibase_person_pin = (
                (
                    polibase_person_list_filtered_result
                    if not A.R.is_empty(polibase_person_list_filtered_result)
                    else polibase_person_list_result
                )
                .data[0]
                .pin
            )
        except NotFound:
            pass

    def recognize_image(self, image: Image.Image, config: RecognizeConfig) -> None:
        self.config = config
        image_width, image_height = image.size
        if config.search_for_polibase_document:
            barcode_information_list: list[
                BarcodeInformation
            ] = self.extruct_barcode_information_from_image(image)
            barcode_information_list = A.D.filter(
                lambda item: item.type
                in A.D.map(lambda item: item, A.CT_P.BARCODE.SUPPORT_FORMATS),
                barcode_information_list,
            )
            if ne(barcode_information_list):
                self.result = RecognizeResult()
                for barcode_information in barcode_information_list:
                    data: int = int(barcode_information.data)
                    if not A.C_P.person_pin(data):
                        return
                    barcode_rect: Rect = barcode_information.rect
                    barcode_bottom: int = barcode_rect[1]
                    barcode_left: int = barcode_rect[0]
                    PADDING: int = 10
                    if barcode_bottom > image_height / 2:
                        self.result.page_correction = PageCorrections.ROTATE_180
                        barcode_bottom = image_height - barcode_bottom - barcode_rect[3]
                        barcode_left = image_width - barcode_left - barcode_rect[2]
                        image = image.transpose(Image.ROTATE_180)
                    if self.logger.level >= 2:
                        self.logger.write_image(
                            "Изображение штрих-код документа",
                            image.crop(
                                (
                                    barcode_left - PADDING,
                                    barcode_bottom - PADDING,
                                    barcode_left + barcode_rect[2] + 2 * PADDING,
                                    barcode_bottom + barcode_rect[3] + PADDING,
                                )
                            ),
                        )
                    polibase_document: A.CT_P_DT = A.CT_P_DT.sorted()[0]
                    polibase_document_description: PolibaseDocumentDescription = (
                        A.D.get(polibase_document)
                    )
                    line_y: float = (
                        barcode_bottom
                        + barcode_rect[3]
                        + polibase_document_description.title_top
                    )
                    image_with_title: Image.Image = image.crop(
                        (
                            0,
                            line_y,
                            image_width,
                            line_y + polibase_document_description.title_height,
                        )
                    )
                    if self.logger.level >= 2:
                        self.logger.write_image(
                            "Изображение заголовка документа", image_with_title
                        )
                    title: str = RecognizeApi.image_to_string(image_with_title)
                    if e(title):
                        pass
                    else:
                        search_polibase_document: A.CT_P_DT | None = (
                            self.get_polibase_document(title)
                        )
                        if e(search_polibase_document):
                            self.result = None
                            return
                        else:
                            self.polibase_document_recognize_result = (
                                PolibaseDocumentRecognizeResult(
                                    search_polibase_document,
                                    barcode_information.type
                                    == A.CT_P.BARCODE.OLD_FORMAT,
                                )
                            )
                    polibase_document_found: bool = ne(
                        self.polibase_document_recognize_result
                    )
                    self.result.polibase_person_pin = data
                    try:
                        self.result.person_name = A.R_P.person_by_pin(
                            self.result.polibase_person_pin
                        ).data.FullName
                        if self.logger.level >= 2:
                            self.logger.write_line(
                                js(("Пациент:", self.result.person_name))
                            )
                    except NotFound:
                        self.result = None
                    if polibase_document_found:
                        result_polibase_document_description: PolibaseDocumentDescription = A.D.get(
                            self.polibase_document_recognize_result.type
                        )
                        if self.logger.level >= 1:
                            self.logger.write_line(
                                f"Заголовок документа Polibase: {result_polibase_document_description.title}"
                            )
                    if ne(self.result):
                        self.result.type = A.CT_DT.POLIBASE
                        if not polibase_document_found:
                            self.logger.error("Тип документа Polibase не определен")
        if config.search_for_direction_document:
            self.result = RecognizeResult()
            self.medical_direction_document_recognize_holder = (
                MedicalDirectionDocumentRecognizeResultHolder(
                    MedicalDirectionDocument()
                )
            )
            # ImageFile.LOAD_TRUNCATED_IMAGES = True
            image_array: np.ndarray = None
            while True:
                try:
                    image_array = np.array(image)
                    break
                except Exception as _:
                    pass
            angle: float | None = determine_skew(
                cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            )
            if angle > 2:
                image_array = RecognizeApi.rotate(image_array, angle)
            max_horizotal_line = RecognizeApi.get_max_horizotal_line(
                image_array, image_height
            )
            if ne(max_horizotal_line):
                (line_x, line_y, line_w, _), lines = max_horizotal_line
                medical_direction_modification_alternative: bool = (
                    image_height - line_y < 350 or line_y < 350
                )
                if (
                    line_y > image_height / 2
                    and not medical_direction_modification_alternative
                ) or (
                    line_y <= image_height / 2
                    and medical_direction_modification_alternative
                ):
                    image_array = RecognizeApi.rotate(image_array, 180)
                    max_horizotal_line = RecognizeApi.get_max_horizotal_line(
                        image_array, image_height
                    )
                    (line_x, line_y, line_w, _), lines = max_horizotal_line
                    self.result.page_correction = PageCorrections.ROTATE_180
                line_width_coefficient: float = line_w / image_width
                if self.logger.level >= 2:
                    for line in lines:
                        cv2.line(
                            image_array,
                            (line[0], line[1]),
                            (line[0] + line[2], line[1]),
                            (0, 255, 0),
                            2,
                        )
                    cv2.line(
                        image_array,
                        (line_x, line_y),
                        (line_x + line_w, line_y),
                        (255, 0, 0),
                        2,
                    )
                    self.logger.write_image(
                        js(
                            (
                                "Линия документа. Коэффициент: ",
                                line_width_coefficient,
                                ". Наклон: ",
                                angle,
                            )
                        ),
                        image_array,
                    )
                if (
                    line_width_coefficient
                    >= MedicalDirectionDocumentDescriptor.minimal_coefficient()
                ):
                    no_medical_direction_line: bool = e(lines)
                    self.medical_direction_document_recognize_holder.modification = (
                        MedicalDirectionDocumentDescriptor.MODIFICATIONS.MODE_ALTERNATIVE
                        if medical_direction_modification_alternative
                        else MedicalDirectionDocumentDescriptor.get_modification(
                            line_width_coefficient
                        )
                    )
                    if ne(
                        self.medical_direction_document_recognize_holder.modification
                    ):
                        document_title_area_rect: tuple[
                            int, int, int, int
                        ] | None = None
                        ogrn_area_rect: tuple[int, int, int, int] | None = None
                        document_title_description: DocumentDescription = DocumentDescription(
                            MedicalDirectionDocumentDescriptor.TITLE,
                            RecognizeApi.STANDART_RATIO,
                            *(
                                MedicalDirectionDocumentDescriptor.STANDART_TTILE_RELATIVE_VALUES
                                if no_medical_direction_line
                                else MedicalDirectionDocumentDescriptor.get_title_area_absolute_values(
                                    self.medical_direction_document_recognize_holder.modification
                                )
                            ),
                        )
                        if no_medical_direction_line:
                            document_title_area_rect = (
                                image_width * document_title_description.left,
                                image_height * document_title_description.top,
                                image_width * document_title_description.right,
                                image_height * document_title_description.bottom,
                            )
                        else:
                            coefficient: float = (
                                1
                                if medical_direction_modification_alternative
                                else line_width_coefficient
                                / MedicalDirectionDocumentDescriptor.get_coefficient(
                                    self.medical_direction_document_recognize_holder.modification
                                )
                            )
                            document_title_area_rect = (
                                0,
                                line_y + document_title_description.top * coefficient,
                                image_width,
                                line_y
                                + document_title_description.bottom * coefficient,
                            )
                            ogrn_area_rect = (
                                0,
                                line_y
                                + MedicalDirectionDocumentDescriptor.get_ogrn_area_absolute_values(
                                    self.medical_direction_document_recognize_holder.modification
                                )[
                                    1
                                ]
                                * coefficient,
                                image_width
                                * MedicalDirectionDocumentDescriptor.get_ogrn_area_relative_width(
                                    self.medical_direction_document_recognize_holder.modification
                                ),
                                line_y
                                + MedicalDirectionDocumentDescriptor.get_ogrn_area_absolute_values(
                                    self.medical_direction_document_recognize_holder.modification
                                )[
                                    3
                                ]
                                * coefficient,
                            )
                        document_title_image_array: np.ndarray = RecognizeApi.crop(
                            image_array, document_title_area_rect
                        )
                        if self.logger.level >= 2:
                            self.logger.write_image(
                                "Изображение заголовка документа",
                                document_title_image_array,
                            )

                        def convert_checker(value: str) -> bool:
                            return (
                                RecognizeApi.get_text_ratio(
                                    value, document_title_description.title, "wr"
                                )
                                > document_title_description.threshold
                            )

                        document_content_area_rect: tuple[
                            int, int, int, int
                        ] | None = None
                        if ne(
                            RecognizeApi.image_to_string(
                                document_title_image_array, convert_checker
                            )
                        ):
                            self.result.type = A.CT_DT.MEDICAL_DIRECTION
                            if self.config.return_only_document_type:
                                return
                            if no_medical_direction_line:
                                document_content_area_rect = (
                                    image_width * 0,
                                    image_height * 0.22,
                                    image_width * 1,
                                    image_height * 0.58,
                                )
                            else:
                                document_content_area_rect = (
                                    document_title_area_rect[0],
                                    document_title_area_rect[1],
                                    document_title_area_rect[2],
                                    line_y
                                    + MedicalDirectionDocumentDescriptor.get_document_content_height(
                                        self.medical_direction_document_recognize_holder.modification
                                    )
                                    * coefficient,
                                )
                            document_content_area_image_array: np.ndarray = (
                                RecognizeApi.crop(
                                    image_array, document_content_area_rect
                                )
                            )
                            document_content_area_image_array = (
                                ImagePreprocessing.magic(
                                    document_content_area_image_array
                                )
                            )
                            ogrn_area_image_array: np.ndarray = (
                                ImagePreprocessing.adaptive_threshold_v1(
                                    ImagePreprocessing.global_threshold(
                                        RecognizeApi.crop(image_array, ogrn_area_rect),
                                        1,
                                    ),
                                    1,
                                )
                            )
                            ogrn_text: str = RecognizeApi.image_to_string(
                                ogrn_area_image_array
                            )
                            self.read_ogrn(ogrn_text)
                            if self.logger.level >= 2:
                                self.logger.write_image(
                                    "Изображение ОГРН", ogrn_area_image_array
                                )
                                self.logger.write_line(
                                    f"Распознавание ОГРН {ogrn_text} -> {self.medical_direction_document_recognize_holder.recognize_result.ogrn_number}"
                                )
                                self.logger.write_image(
                                    "Изображение направления",
                                    document_content_area_image_array,
                                )
                            document_content_text: str = RecognizeApi.image_to_string(
                                document_content_area_image_array
                            )
                            reader_list: list = [
                                self.read_medical_direction_number_and_date,
                                self.read_person_ensurence_number,
                                self.read_person_name,
                                self.read_person_birthday,
                                self.read_medical_research_type,
                            ]
                            for line in document_content_text.splitlines():
                                index: int = 0
                                for _ in reader_list:
                                    reader_item: Callable[
                                        [str], bool | None
                                    ] = reader_list[index]
                                    result: bool | None = reader_item(line)
                                    if result == False:
                                        index += 1
                                    else:
                                        if result:
                                            reader_list.pop(0)
                                        break
                                if e(reader_list):
                                    break
                            if ne(
                                self.medical_direction_document_recognize_holder.recognize_result.number
                            ):
                                self.find_polibase_person()
                        else:
                            self.result = None
                    else:
                        self.result = None
                else:
                    self.result = None
            else:
                self.result = None
