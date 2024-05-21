import ipih

from pih import A
from RecognizeService.const import *

SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:
    if A.U.for_service(SD):

        from pih.collections import (
            PolibaseDocument,
            BarcodeInformation,
            ChillerIndicationsValue,
            MedicalDirectionDocument,
            PolibaseDocumentDescription,
        )

        from RecognizeService.api import (
            RecognizeResult,
            RecognizeConfig,
            RecognizeApi as Api,
            MedicalDirectionDocument,
            PolibaseDocumentRecognizeResult,
            MedicalDirectionDocumentRecognizeResultHolder,
        )
        from pih.consts.errors import Redirection
        from pih_tls import Converter, Logger
        from MobileHelperService.client import Client as MIO
        from pih.tools import ParameterList, ne, e, nn, j, b, js

        from typing import Any
        from PIL import Image
        import grpc
        import time

        logger: Logger = Logger(
            MIO.create_output(A.CT_ME_WH.GROUP.DOCUMENTS_WORK_STACK)
        )

        recognize_api: Api = Api(logger)

        def recognize_display(indications_value: ChillerIndicationsValue) -> None:
            recognize_api.recognize_display(indications_value)

        def service_call_handler(sc: SC, parameter_list: ParameterList) -> Any:
            if sc == SC.register_chiller_indications_value:
                indications_value: ChillerIndicationsValue = parameter_list.next(
                    ChillerIndicationsValue()
                )
                if e(indications_value.temperature):
                    recognize_display(indications_value)
                return indications_value
            if sc == SC.recognize_document:
                path: str = parameter_list.next()
                document_type: A.CT_DT | None = A.D.get_by_value(
                    A.CT_DT, parameter_list.next()
                )
                try:
                    result: (
                        bool | PolibaseDocument | list[MedicalDirectionDocument] | None
                    ) = recognize_document(
                        path,
                        document_type,
                        parameter_list.next(),
                        parameter_list.next(),
                    )
                    return A.R.pack(
                        (
                            A.CT_FCA.VALUE_LIST
                            if isinstance(result, list)
                            else A.CT_FCA.VALUE
                        ),
                        result,
                    )
                except Redirection as redirection:
                    return redirection.arg

            if sc == SC.document_type_exists:
                return recognize_document(
                    parameter_list.next(),
                    A.D.get_by_value(A.CT_DT, parameter_list.next()),
                    True,
                    parameter_list.next(),
                )
            if sc == SC.get_barcode_list_information:
                source_file_path: str = parameter_list.next()
                _: bool = parameter_list.next()
                log_level: int | None = parameter_list.next()
                logger.level = log_level
                source_file_extension: str = A.PTH.get_extension(source_file_path)
                pdf_format_detected: bool = source_file_extension == A.CT_F_E.PDF
                image_format_detected: bool = source_file_extension in [
                    A.CT_F_E.JPEG,
                    A.CT_F_E.JPG,
                ]
                page_image_list: list[Image.Image] | None = None
                if pdf_format_detected or image_format_detected:
                    while True:
                        try:
                            page_image_list = (
                                Converter.pdf_to_pages_as_image_list(source_file_path)
                                if pdf_format_detected
                                else [Image.open(source_file_path)]
                            )
                            break
                        except Exception as _:
                            time.sleep(2)
                    result: list[list[BarcodeInformation]] = []
                    if len(page_image_list) > 0:
                        for page_image in page_image_list:
                            barcode_information_list: list[BarcodeInformation] = (
                                recognize_api.extruct_barcode_information_from_image(
                                    page_image
                                )
                            )
                            result.append(barcode_information_list)
                    return A.R.pack(A.CT_FCA.VALUE_LIST, result)
            return None

        def recognize_document(
            document_file_path: str,
            document_type: A.CT_DT | None = None,
            check_only_document_type: bool = False,
            log_level: int | None = None,
        ) -> bool | PolibaseDocument | list[MedicalDirectionDocument] | None:
            recognize_result: RecognizeResult | None = None
            logger.level = log_level
            #
            document_file_name: str = A.PTH.get_file_name(document_file_path).lower()
            document_file_extension: str = A.PTH.get_extension(document_file_path)
            #
            pdf_format_detected: bool = document_file_extension == A.CT_F_E.PDF
            image_format_detected: bool = (
                not pdf_format_detected
                and document_file_extension in [A.CT_F_E.JPEG, A.CT_F_E.JPG]
            )
            #
            if pdf_format_detected or image_format_detected:
                source_file_directory: str = A.PTH.get_file_directory(
                    document_file_path
                )
                test_scanned_file_detected: bool = source_file_directory == A.PTH.path(
                    A.PTH.SCAN_TEST.VALUE
                )
                if nn(document_type):
                    page_list: list[Image.Image] | None = None
                    if A.PTH.exists(document_file_path):
                        while True:
                            try:
                                page_list = (
                                    Converter.pdf_to_pages_as_image_list(
                                        document_file_path
                                    )
                                    if pdf_format_detected
                                    else [Image.open(document_file_path)]
                                )
                                break
                            except Exception as _:
                                time.sleep(2)
                    else:
                        raise Redirection(
                            A.ER.rpc(
                                message=js(("Файл", document_file_path, "не найден")),
                                code=grpc.StatusCode.NOT_FOUND,
                            )
                        )
                    if len(page_list) > 0:
                        page_image: Image.Image = page_list[0]
                        # page_image.show()
                        if log_level >= 1:
                            scan_source_title: str | None = None
                            for scan_source_item in A.CT_SCN.Sources:
                                scan_source_item_value: tuple[str, str] = A.D.get(
                                    scan_source_item
                                )
                                if document_file_name.startswith(
                                    scan_source_item_value[0]
                                ):
                                    scan_source_title = scan_source_item_value[1]
                                    break
                            if test_scanned_file_detected:
                                scan_source_title = A.D.get(A.CT_SCN.Sources.TEST)[1]
                            if ne(scan_source_title):
                                logger.write_image(
                                    j(
                                        (
                                            "Входящий документ: ",
                                            A.PTH.add_extension(
                                                document_file_name,
                                                document_file_extension,
                                            ),
                                            " (",
                                            b(scan_source_title),
                                            ")",
                                        )
                                    ),
                                    page_image,
                                )
                        recognize_result_map: dict[int, RecognizeResult] = {}
                        polibase_document_recognize_result_map: dict[
                            int, PolibaseDocument
                        ] = {}
                        if document_type == A.CT_DT.POLIBASE:
                            page_index: int = 0
                            page: Image.Image = page_list[page_index]
                            recognize_api = Api(logger)
                            recognize_api.recognize_image(
                                page,
                                RecognizeConfig(True, False),
                            )
                            recognize_result = recognize_api.result
                            if check_only_document_type:
                                return (
                                    nn(recognize_result)
                                    and recognize_result.type == document_type
                                )
                            if ne(recognize_result):
                                polibase_scanned_document: PolibaseDocument | None = (
                                    None
                                )
                                recognize_result_map[page_index] = recognize_result
                                polibase_document_recognize_result: (
                                    PolibaseDocumentRecognizeResult | None
                                ) = recognize_api.polibase_document_recognize_result
                                if ne(polibase_document_recognize_result):
                                    polibase_document_recognize_result_map[
                                        page_index
                                    ] = polibase_document_recognize_result
                                    polibase_document_description: (
                                        PolibaseDocumentDescription
                                    ) = A.D.get(polibase_document_recognize_result.type)
                                    for medical_direction_index in range(
                                        polibase_document_description.page_count - 1
                                    ):
                                        recognize_result_map[
                                            page_index + medical_direction_index + 1
                                        ] = recognize_result
                                        polibase_document_recognize_result_map[
                                            page_index + medical_direction_index + 1
                                        ] = polibase_document_recognize_result
                                    if not test_scanned_file_detected and ne(
                                        polibase_document_recognize_result
                                    ):
                                        polibase_scanned_document = PolibaseDocument(
                                            document_file_path,
                                            recognize_result.polibase_person_pin,
                                            polibase_document_recognize_result.type.name,
                                        )
                                    return polibase_scanned_document
                                else:
                                    return None
                        medical_direction_document_result_map: dict[
                            int, MedicalDirectionDocumentRecognizeResultHolder
                        ] = {}
                        if document_type == A.CT_DT.MEDICAL_DIRECTION:
                            for page_index, page in enumerate(page_list):
                                if page_index in recognize_result_map:
                                    continue
                                recognize_api = Api(logger)
                                recognize_api.recognize_image(
                                    page,
                                    RecognizeConfig(False, True, False),
                                )
                                recognize_result = recognize_api.result
                                if check_only_document_type:
                                    return (
                                        nn(recognize_result)
                                        and recognize_result.type == document_type
                                    )
                                if ne(recognize_result):
                                    recognize_result_map[page_index] = recognize_result
                                    if (
                                        recognize_result.type
                                        == A.CT_DT.MEDICAL_DIRECTION
                                    ):
                                        medical_direction_document_result_map[
                                            page_index
                                        ] = (
                                            recognize_api.medical_direction_document_recognize_holder.recognize_result
                                        )
                            if ne(medical_direction_document_result_map):
                                result: list[MedicalDirectionDocument] = A.D.as_list(
                                    medical_direction_document_result_map
                                )

                                def config(value: MedicalDirectionDocument) -> None:
                                    value.person_name = recognize_result.person_name

                                return A.D.every(config, result)
                            """
                            medical_direction_document: MedicalDirectionDocument = (
                                medical_direction_document_result_map[0]
                            )
                            result_with_person_name: RecognizeResult | None = None
                            if ne(recognize_result_map):
                                for page_index in recognize_result_map:
                                    value: RecognizeResult = recognize_result_map[
                                        page_index
                                    ]
                                    if ne(value.person_name) and ne(
                                        value.person_name
                                    ):
                                        result_with_person_name = value
                                        break
                                has_person_name: bool = ne(result_with_person_name)
                                medical_direction_type_string: str = j(
                                    A.D.map(
                                        lambda item: item.type.alias,
                                        A.D.filter(
                                            lambda item: ne(item.type),
                                            medical_direction_document_result_map,
                                        ),
                                    ),
                                    ", ",
                                )
                                if has_person_name:
                                    name_list: list[str] = A.D.split_with_not_empty_items(
                                        result_with_person_name.person_name, " "
                                    )
                                    person_name_string = js(
                                        (
                                            A.D.capitalize(name_list[0].lower()),
                                            j(
                                                A.D.map(
                                                    lambda item: str(item[0]).upper(),
                                                    name_list[1:],
                                                ),
                                                ". ",
                                            ),
                                        )
                                    )
                                today: datetime = A.D.today(as_datetime=True)
                                year_string: str = str(today.year)
                                result_path: str = A.PTH.join(A.PTH.OMS.VALUE, "Done")
                                result_path = A.PTH.join(result_path, year_string)
                                A.PTH.make_directory_if_not_exists(result_path)
                                result_path = A.PTH.join(
                                    result_path,
                                    A.D.datetime_to_string(
                                        today, A.CT.YEARLESS_DATE_FORMAT
                                    ),
                                )
                                A.PTH.make_directory_if_not_exists(result_path)
                                result_path = A.PTH.join(
                                    result_path,
                                    A.PTH.add_extension(
                                        j(
                                            (
                                                person_name_string,
                                                ". Направление ",
                                                medical_direction_type_string,
                                            )
                                        ),
                                        document_file_extension,
                                    ),
                                )
                                preresult_path: str = A.PTH.join(
                                    A.PTH.APP_DATA.OCR_RESULT_FOLDER,
                                    A.PTH.add_extension(A.D.uuid(), A.CT_F_E.PDF),
                                )
                                ocr_pdf_writer = PdfWriter()
                                source_pdf_reader = PdfReader(document_file_path, "rb")

                                def rotate_page(
                                    result: RecognizeResult, page: PageObject
                                ) -> None:
                                    if page_index in recognize_result_map:
                                        page_correction: PageCorrections | None = (
                                            result.page_correction
                                        )
                                        if (
                                            page_correction
                                            == PageCorrections.ROTATE_90_COUNTER
                                        ):
                                            page.rotate(-90)
                                        if page_correction == PageCorrections.ROTATE_90:
                                            page.rotate(90)
                                        if page_correction == PageCorrections.ROTATE_180:
                                            page.rotate(180)

                                for page_index in recognize_result_map:
                                    result = recognize_result_map[page_index]
                                    if (
                                        ne(result.type)
                                        and result.type == A.CT_DT.MEDICAL_DIRECTION
                                    ):
                                        rotate_page(
                                            result, source_pdf_reader.pages[page_index]
                                        )
                                        ocr_pdf_writer.add_page(
                                            source_pdf_reader.pages[page_index]
                                        )
                                for page_index in recognize_result_map:
                                    result = recognize_result_map[page_index]
                                ocr_pdf_file_path: str = A.PTH.join(
                                    A.PTH.APP_DATA.OCR_RESULT_FOLDER,
                                    A.PTH.add_extension(A.D.uuid(), A.CT_F_E.PDF),
                                )
                                with open(
                                    ocr_pdf_file_path,
                                    # if TEST_SETTINGS.ocr
                                    # else preresult_path,
                                    "wb",
                                ) as file:
                                    ocr_pdf_writer.write(file)
                                sidecar_path: str = A.PTH.join(
                                    A.PTH.APP_DATA.OCR_RESULT_FOLDER,
                                    A.PTH.add_extension(A.D.uuid(), A.CT_F_E.TXT),
                                )
                                ocrmypdf.ocr(
                                    ocr_pdf_file_path,
                                    preresult_path,
                                    language=["rus"],
                                    deskew=True,
                                    clean=True,
                                    clean_final=True,
                                    sidecar=sidecar_path,
                                )
                                #
                                text_contents: str | None = None
                                with open(sidecar_path, "r", encoding="UTF-8") as file:
                                    text_contents = file.readlines()
                                try:
                                    result_pdf_file = PdfReader(open(preresult_path, "rb"))
                                    packet = BytesIO()
                                    pdfmetrics.registerFont(
                                        TTFont(
                                            A.CT_FNT.FOR_PDF,
                                            A.PTH_FNT.get(A.CT_FNT.FOR_PDF),
                                            "UTF-8",
                                        )
                                    )
                                    canvas = Canvas(packet, pagesize=A4)
                                    textobject = canvas.beginText(20, 200)
                                    textobject.setFont(A.CT_FNT.FOR_PDF, 11)
                                    result_text: str = (
                                        f"Пациент: {result_with_person_name.person_name}\n"
                                    )
                                    for (
                                        medical_direction_index,
                                        page_index,
                                    ) in enumerate(medical_direction_document_result_map):
                                        medical_direction_document_recognize_result: MedicalDirectionDocumentRecognizeResult = medical_direction_document_result_map[
                                            page_index
                                        ]
                                        result_text += f"Направление {medical_direction_index + 1}: {medical_direction_document_recognize_result.number}\n"
                                        ogrn: OGRN | None = A.R_DS.ogrn(
                                            medical_direction_document_recognize_result.ogrn_number
                                        ).data
                                        if ne(ogrn):
                                            result_text += (
                                                f"   Мед. учереждение: {ogrn.name}\n"
                                            )
                                        result_text += f"   Тип: {medical_direction_document_recognize_result.type_code} ({medical_direction_document_recognize_result.type.alias})\n"
                                        result_text += f"   Дата: {A.D.datetime_to_string(medical_direction_document_recognize_result.date, A.CT.DATE_FORMAT)}\n"
                                    result_text += f"Дата рождения: {A.D.datetime_to_string(medical_direction_document_recognize_result.person_birthday, A.CT.DATE_FORMAT)}\n"
                                    result_text += f"Номер страхового полюса: {medical_direction_document_recognize_result.person_ensurence_number}\n"
                                    result_text += f"Страхователь: {medical_direction_document_recognize_result.person_ensurence_agent}\n"
                                    if log_level >= 1:
                                        logger.write_line(result_text)
                                    width, _ = A4
                                    canvas.setFillColor(black)
                                    canvas.rect(
                                        20, 10, width - 40, 200, stroke=True, fill=True
                                    )
                                    canvas.setFillColor(white)
                                    for line in result_text.splitlines(False):
                                        textobject.textLine(line.rstrip())
                                    canvas.drawText(textobject)

                                    canvas.save()
                                    packet.seek(0)
                                    modificated_pdf_file = PdfReader(packet)
                                    result_output = PdfWriter()
                                    for page_index, page in enumerate(
                                        result_pdf_file.pages
                                    ):
                                        if page_index == 0:
                                            page.merge_page(
                                                modificated_pdf_file.pages[page_index]
                                            )
                                        result_output.add_page(page)
                                    for (
                                        page_index
                                    ) in polibase_document_recognize_result_map:
                                        polibase_document_recognize_result: MedicalDirectionDocument = polibase_document_recognize_result_map[
                                            page_index
                                        ]
                                        result_output.add_page(
                                            source_pdf_reader.pages[page_index]
                                        )
                                    with open(result_path, "wb") as result_output_stream:
                                        result_output.write(result_output_stream)
                                    if test_scanned_file_detected:
                                        os.remove(document_file_path)
                                except Exception as error:
                                    shutil.move(preresult_path, result_path)
                                    logger.error(f"Ошибка аннотации документа {error}")
                            else:
                                pass
                        """
            return None

        def service_starts_handler() -> None:
            A.SRV_A.subscribe_on(
                SC.register_chiller_indications_value, A.CT_SubT.ON_PARAMETERS
            )

        A.SRV_A.serve(
            SD,
            service_call_handler,
            service_starts_handler,
            isolate=ISOLATED,
            as_standalone=as_standalone,
        )


if __name__ == "__main__":
    start()
