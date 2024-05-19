from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import ApiRequestError
from io import BytesIO
from typing import BinaryIO
from flexidata.Logger import Logger
from flexidata.reader.file_reader import FileReader
logger = Logger()

class GoogleDriveFileReader(FileReader):
    def __init__(self, file_id):
        self.file_id = file_id

    def read_file(self) -> BinaryIO:
        try:
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            drive = GoogleDrive(gauth)
            file = drive.CreateFile({'id': self.file_id})
            file.FetchContent()
            return BytesIO(file.content)
        except ApiRequestError as e:
            logger.error(f"API request error from Google Drive: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while accessing Google Drive: {e}")
            raise
