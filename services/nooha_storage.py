from typing import BinaryIO, Final
import boto3
from fastapi import UploadFile
from utils.str_utils import get_file_extension
from models.nooha import Nooha


class NoohaStorage:

    BUCKET_NAME: Final = 'noohas'

    def __init__(self, s3_client = None):
        self.s3_client = s3_client

    def upload_nooha(self, file: UploadFile, nooha: Nooha):
        extension = get_file_extension(file.filename)
        if extension not in ['mp3', 'mp4']:
            raise ValueError('The file can be either audio or video')
        self.s3_client.upload_fileobj(
            file.file,
            self.BUCKET_NAME,
            file.filename,
        )
        return file.filename

    def get_public_nooha_url(self, nooha: Nooha):
        if nooha.aws_key is None or len(nooha.aws_key) == 0:
            return ''
        return f"https://{self.BUCKET_NAME}.s3.amazonaws.com/{nooha.aws_key}"

    def delete_nooha(self, key: str):
        self.s3_client.delete_object(
            Bucket=self.BUCKET_NAME,
            Key=key
        )

    def list_noohas(self):
        self.s3_client.list_objects_v2(
            self.BUCKET_NAME
        )