import re

UNICODE_BULLETS = [
    "\u0095",
    "\u2022",
    "\u2023",
    "\u2043",
    "\u3164",
    "\u204C",
    "\u204D",
    "\u2219",
    "\u25CB",
    "\u25CF",
    "\u25D8",
    "\u25E6",
    "\u2619",
    "\u2765",
    "\u2767",
    "\u29BE",
    "\u29BF",
    "\u002D",
    "",
    "*",
    "\x95",
    "·",
]


class ElementType:
    PARAGRAPH = "Paragraph"
    IMAGE = "Image"
    PARAGRAPH_IN_IMAGE = "ParagraphInImage"
    FIGURE = "Figure"
    PICTURE = "Picture"
    TABLE = "Table"
    PARAGRAPH_IN_TABLE = "ParagraphInTable"
    LIST = "List"
    FORM = "Form"
    PARAGRAPH_IN_FORM = "ParagraphInForm"
    CHECK_BOX_CHECKED = "CheckBoxChecked"
    CHECK_BOX_UNCHECKED = "CheckBoxUnchecked"
    RADIO_BUTTON_CHECKED = "RadioButtonChecked"
    RADIO_BUTTON_UNCHECKED = "RadioButtonUnchecked"
    LIST_ITEM = "List-item"
    FORMULA = "Formula"
    CAPTION = "Caption"
    PAGE_HEADER = "Page-header"
    SECTION_HEADER = "Section-header"
    PAGE_FOOTER = "Page-footer"
    FOOTNOTE = "Footnote"
    TITLE = "Title"
    TEXT = "Text"
    UNCATEGORIZED_TEXT = "UncategorizedText"
    PAGE_BREAK = "PageBreak"
    CODE_SNIPPET = "CodeSnippet"
    PAGE_NUMBER = "PageNumber"
    OTHER = "Other"


class ParserMethod:
    AUTO = "auto"
    FAST = "fast"
    OCR = "ocr"
    MODEL = "model"


class FileType:
    PDF = "application/pdf"

class FileReaderSource:
    WEB_URL = "web_url"
    LOCAL = "local"
    S3 = "s3"
    GOOGLE_DRIVE = "google_drive"

class EXTRACTIONSOURCE:
    PDF_MINER = "pdfminer.six"

class OCREngine:
    TESSERACT = "tesseract"
    PADDLE = "paddle"
    GOOGLE_VISION = "google_vision"


class Patterns:
    WHITESPACE_NEWLINE_PATTERN = r"\s*\n\s*"
    END_WITH_PUNCTUATION = r"[^\w\s]\Z"
    LIST_ITEM_REGEX = re.compile(
        r"^([" + "".join(UNICODE_BULLETS) + r"]|\d+\)|\d+\.\s|\d+\])\s"
    )
    NUMERIC_REGEX = r'^[-+~]?(\d{1,3}(,\d{3})*|\d+)(\.\d+)?$'
