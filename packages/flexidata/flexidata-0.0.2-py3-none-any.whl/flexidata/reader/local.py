from io import BytesIO
from typing import BinaryIO
from flexidata.Logger import Logger
from flexidata.reader.file_reader import FileReader
logger = Logger()

class LocalFileReader(FileReader):
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    def read_file(self) -> BinaryIO:
        try:
            with open(self.file_path, 'rb') as file:
                return BytesIO(file.read())
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            raise
        except PermissionError:
            logger.error(f"Permission denied for file: {self.file_path}")
            raise
        except Exception as e:
            logger.error(f"An error occurred while reading the file: {e}")
            raise
