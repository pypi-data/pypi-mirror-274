import unittest
from flexidata.parser.pdf import PDFParser
from flexidata.utils.constants import FileReaderSource, ParserMethod
import unittest
from flexidata.parser.pdf import PDFParser
from flexidata.utils.constants import FileReaderSource, ParserMethod


class TestPDFParser(unittest.TestCase):
    def test_init(self):
        parser = PDFParser(
            file_path="/app/flexi-data/example-docs/2404.19553v1.pdf",
            source=FileReaderSource.LOCAL,
            method=ParserMethod.OCR,
            extract_image=True,
        )
        self.assertIsInstance(parser, PDFParser)

    def test_get_file_content(self):
        parser = PDFParser()
        content = parser.get_file_content()
        self.assertEqual(content, None)

    def test_set_parser_auto_method(self):
        parser = PDFParser()
        parser.set_parser_auto_method()
        self.assertEqual(parser.method, ParserMethod.AUTO)

    def test_parse(self):
        parser = PDFParser()
        result = parser.parse()
        self.assertEqual(result, None)

    def test_parse_by_model(self):
        parser = PDFParser()
        result = parser.parse_by_model()
        self.assertEqual(result, None)

    def test_parse_by_ocr(self):
        parser = PDFParser()
        result = parser.parse_by_ocr()
        self.assertEqual(result, None)

    def test_convert_pdf_to_image(self):
        parser = PDFParser()
        result = parser.convert_pdf_to_image()
        self.assertEqual(result, None)

    def test_process_images(self):
        parser = PDFParser()
        result = parser.process_images([])
        self.assertEqual(result, None)

    def test_annotation_resolve(self):
        parser = PDFParser()
        result = parser.annotation_resolve(None)
        self.assertEqual(result, None)

    def test_get_urls(self):
        parser = PDFParser()
        result = parser.get_urls([], 1, 100)
        self.assertEqual(result, None)

    def test_extract_text_from_img_with_rapidocr(self):
        parser = PDFParser()
        result = parser.extract_text_from_img_with_rapidocr([])
        self.assertEqual(result, None)

    def test_parse_by_pdfminer(self):
        parser = PDFParser()
        result = parser.parse_by_pdfminer()
        self.assertEqual(result, None)

    def test_extract_text(self):
        parser = PDFParser()
        result = parser.extract_text(None)
        self.assertEqual(result, None)

    def test_get_pdfminer_pages(self):
        parser = PDFParser()
        result = parser.get_pdfminer_pages(None)
        self.assertEqual(result, None)

        if __name__ == '__main__':
            unittest.main()
