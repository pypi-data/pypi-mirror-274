import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from io import BytesIO
from typing import BinaryIO
from flexidata.Logger import Logger
from flexidata.reader.file_reader import FileReader
logger = Logger()

class S3FileReader(FileReader):
    def __init__(self, bucket_name, file_key):
        self.bucket_name = bucket_name
        self.file_key = file_key

    def read_file(self) -> BinaryIO:
        try:
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=self.bucket_name, Key=self.file_key)
            return BytesIO(response['Body'].read())
        except NoCredentialsError:
            logger.error("AWS credentials not available")
            raise
        except PartialCredentialsError:
            logger.error("Incomplete AWS credentials")
            raise
        except ClientError as e:
            logger.error(f"Client error in AWS S3 access: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise
