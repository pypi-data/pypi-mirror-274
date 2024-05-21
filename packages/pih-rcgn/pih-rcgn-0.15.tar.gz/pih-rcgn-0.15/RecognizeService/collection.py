from dataclasses import dataclass, field

import ipih

from RecognizeService.const import PageCorrections
from pih.collections import MedicalDirectionDocument
from pih.consts.polibase import PolibaseDocumentTypes


@dataclass
class PersonDocumentTypeDescription:
    name: str
    width: int
    height: int


@dataclass
class RecognizeResult:
    person_name: str | None = None
    polibase_person_pin: int | None = None
    type: int | None = None
    page_correction: PageCorrections | None = None



@dataclass
class RecognizeConfig:
    search_for_polibase_document: bool = True
    search_for_direction_document: bool = True
    return_only_document_type: bool = False


@dataclass
class PolibaseDocumentRecognizeResult:
    type: PolibaseDocumentTypes | None = None
    barcode_old_format: bool | None = None


@dataclass
class MedicalDirectionDocumentRecognizeResultHolder:
    recognize_result: MedicalDirectionDocument | None = None
    type_line_found: bool = False
    type_line_list: list[str] = field(default_factory=lambda: [])
    type_ratio_list: list[tuple[str, int, str]] = field(
        default_factory=lambda: []
    )
    modification: int | None = None
