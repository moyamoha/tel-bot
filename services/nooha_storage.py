from typing import BinaryIO
import boto3
from fastapi import UploadFile
from utils.str_utils import get_file_extension
from models.nooha import Nooha


class NoohaStorage:

    BUCKET_NAME = 'noohas'

    def __init__(self, s3_client = None):
        self.s3_client = s3_client

    def upload_nooha(self, file: UploadFile, nooha: Nooha):
        extension = get_file_extension(file.filename)
        # if extension not in ['mp3', 'mp4']:
        #     raise ValueError('File can either be audio or video')
        key = f"{nooha.id}___{file.filename}"
        self.s3_client.upload_fileobj(
            file.file,
            self.BUCKET_NAME,
            key,
        )
        return key

    def download_nooha(self):
        pass

    def delete_nooha(self):
        pass

    def list_noohas(self):
        pass