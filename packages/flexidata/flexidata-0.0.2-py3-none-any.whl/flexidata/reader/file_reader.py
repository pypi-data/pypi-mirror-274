from abc import ABC, abstractmethod
from typing import BinaryIO

from flexidata.Logger import Logger
from io import BytesIO
from flexidata.utils.constants import FileReaderSource
logger = Logger()

class FileReader(ABC):

    @abstractmethod
    def read_file(self) -> BinaryIO:
        pass
    
