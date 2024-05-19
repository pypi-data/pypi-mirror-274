import requests
from requests.exceptions import HTTPError, RequestException
from io import BytesIO
from typing import BinaryIO
from flexidata.Logger import Logger
from flexidata.reader.file_reader import FileReader
logger = Logger()

class WebFileReader(FileReader):
    def __init__(self, url):
        self.url = url

    def read_file(self) -> BinaryIO:
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return BytesIO(response.content)
        except HTTPError as e:
            logger.error(f"HTTP error occurred while requesting {self.url}: {e}")
            raise
        except RequestException as e:
            logger.error(f"Error occurred while requesting {self.url}: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while accessing {self.url}: {e}")
            raise
