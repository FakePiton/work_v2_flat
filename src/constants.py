from enum import Enum

class Action(Enum):
    CREATE_TEMPLATE_ORDER = "create_template_order"
    MERGE_PDF = "merge"
    REPORT_MESSAGE = "report_message"
    RESET_DB = "reset_db"
    DECLENSION = "declension"


class Sheet(Enum):
    ARROWS = "Arrows"
    DECLENSION = "declension"
    LEAVE = "ВІДПУ"
    BASE_2 = "base_2"
    SH = "sh"
    HV = "ХВ"
    DFFK = "ДПНП"


class CaseLanguage(Enum):
    ACCUSATIVE = "accusative"  # знахідний
    DATIVE = "dative"  # давальний


class PATH(Enum):
    PATH_EXCEL = "path_excel"
    PATH_SERVER_ORDER = "path_server_order"
    PATH_FILES_PDF = "path_files_pdf"
    PATH_DIR_DECLENSION = "path_dir_declension"
