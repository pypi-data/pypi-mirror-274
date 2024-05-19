from flexidata.utils.constants import FileReaderSource
from flexidata.reader.local import LocalFileReader
from flexidata.reader.s3 import S3FileReader
from flexidata.reader.google_drive import GoogleDriveFileReader
from flexidata.reader.web import WebFileReader


def get_file_reader(source_type, **kwargs):
    if source_type == FileReaderSource.LOCAL:
        return LocalFileReader(**kwargs)
    elif source_type == FileReaderSource.S3:
        return S3FileReader(**kwargs)
    elif source_type == FileReaderSource.GOOGLE_DRIVE:
        return GoogleDriveFileReader(**kwargs)
    elif source_type == FileReaderSource.WEB_URL:
        return WebFileReader(**kwargs)
    else:
        raise ValueError("Unsupported source type")
