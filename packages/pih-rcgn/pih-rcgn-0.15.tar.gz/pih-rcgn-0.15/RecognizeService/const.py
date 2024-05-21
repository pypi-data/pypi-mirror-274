import ipih

from pih.collections.service import ServiceDescription
from pih.consts.hosts import Hosts
from pih.tools import j

from enum import IntEnum, auto

NAME: str = "Recognize"

HOST = Hosts.WS255

PACKAGES: tuple[str, ...] =  (
        "fuzzywuzzy",
        "pyzbar",
        "opencv-python",
        "pytesseract",
        "ocrmypdf",
        "PyPDF2",
        "reportlab",
        "python-Levenshtein",
        "numpy",
        "opencv-python",
        "deskew"
    )

VERSION: str = "0.15"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Recognize service",
    host=HOST.NAME,
    host_changeable=False,
    commands=(
        "get_barcode_list_information",
        "document_type_exists",
        "recognize_document",
    ),
    use_standalone=True,
    standalone_name="rcgn",
    version=VERSION,
    packages=PACKAGES,
)

LOG_LEVEL: int = 2


class PageCorrections(IntEnum):
    ROTATE_90 = auto()
    ROTATE_90_COUNTER = auto()
    ROTATE_180 = auto()


class MedicalDirectionDocumentDescriptor:
    
    TITLE: str = "Направление №"
    OGRN_TITLE: str = "код огрн"

    @staticmethod
    def get_person_polis_title(modification: int) -> str:
        return j(
            (
                "1. Номер",
                [" страхового полиса", ""][
                    modification
                    == MedicalDirectionDocumentDescriptor.MODIFICATIONS.MODE_ALTERNATIVE
                ],
            )
        )

    @staticmethod
    def get_medical_direction_type_title(modification: int) -> str | None:
        if modification == MedicalDirectionDocumentDescriptor.MODIFICATIONS.NORMAL:
            return "8: Обоснование направления Цель обращения:"
        if modification == MedicalDirectionDocumentDescriptor.MODIFICATIONS.MODE_1:
            return "8: Обоснование направления"
        if modification == MedicalDirectionDocumentDescriptor.MODIFICATIONS.MODE_ALTERNATIVE:
            return "8."

    @staticmethod
    def get_person_name_title(modification: int) -> str:
        result: str = "3. Фамилия,"
        if modification != MedicalDirectionDocumentDescriptor.MODIFICATIONS.MODE_ALTERNATIVE:
            result += " имя, отчество"
        return result

    @staticmethod
    def get_birthday_title(modification: int) -> str:
        result: str = "4. Дата"
        if modification != MedicalDirectionDocumentDescriptor.MODIFICATIONS.MODE_ALTERNATIVE:
            result += " рождения"
        return result

    MODIFICATION_COEFFICIENT_LIST: list[tuple[float, float]] = [
        (1, 0.75),
        (0.74, 0.65),
    ]

    @staticmethod
    def get_coefficient(modification: int) -> float:
        return [0.9, 0.71][modification]

    @staticmethod
    def minimal_coefficient() -> float:
        max_value: float = 1
        for item in MedicalDirectionDocumentDescriptor.MODIFICATION_COEFFICIENT_LIST:
            max_value = min(max_value, item[1])
        return max_value

    @staticmethod
    def get_modification(coefficient: float) -> int | None:
        for index, item in enumerate(
            MedicalDirectionDocumentDescriptor.MODIFICATION_COEFFICIENT_LIST
        ):
            if item[0] >= coefficient and item[1] < coefficient:
                return index
        return None

    @staticmethod
    def get_title_area_absolute_values(modification: int) -> tuple[int, int, int, int]:
        return [(0, -250, 0, -120), (0, -180, 0, -90), (0, -1680, 0, -1450)][
            modification
        ]

    @staticmethod
    def get_ogrn_area_absolute_values(modification: int) -> tuple[int, int, int, int]:
        return [(0, -300, 0, -220), (0, -450, 0, -370), (0, -1700, 0, -1650)][
            modification
        ]

    @staticmethod
    def get_ogrn_area_relative_width(modification: int) -> float:
        return [0.3, 0.4, 0.4][modification]

    @staticmethod
    def get_document_content_height(modification: int) -> int:
        return [580, 480, -200][modification]

    STANDART_TTILE_RELATIVE_VALUES: tuple[float, float, float, float] = (
        0.5444,
        0.0855,
        1,
        0.171,
    )

    class MODIFICATIONS:
        NORMAL: int = 0
        MODE_1: int = 1
        MODE_ALTERNATIVE: int = 2


CORRECTION_TABLE: dict[str, list[tuple[str, list[str]]]] = {
    "date": [(".", [":", ",", " "])]
}


class BARCODE:
    RELATIVE_AREA_HEIGHT: float = 0.3
