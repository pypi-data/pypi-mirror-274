'''
@File    :   self._s3.py
@Time    :   2022/07/11 15:04:30
@Author  :   susufqx
@Version :   1.0
@Contact :   jiangsulirui@gmail.com
'''


import os
import boto3
import urllib3
from boto3.resources.base import ServiceResource as s3_cls
from typing import Tuple
from urllib.parse import quote

from .log import logger, print_excp
from .crypto import CryptoUtil


urllib3.disable_warnings()


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class S3:
    def __init__(self, access_key: str, secret_key: str, s3_base_url: str, **config) -> None:
        self._bucket = config.get("bucket")
        self._access_key = access_key
        self._secret_key = secret_key
        self._s3_base_url = s3_base_url
        self._s3 = boto3.resource(
            service_name='s3',
            region_name='asr',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=self._s3_base_url,
            verify=False,
        )

        self.__create_bucket()

    def __check_bucket(self) -> Tuple[bool, object]:
        for i in self._s3.buckets.all():
            if i.name == self._bucket:
                return (True, i)
        return (False, None)

    def __create_bucket(self) -> None:
        exist, _ = self.__check_bucket()
        if not exist:
            try:
                self._s3.create_bucket(Bucket=self._bucket)
            except Exception as e:
                print_excp(e)
                logger.info(f"create bucket {self._bucket} failed")
            else:
                logger.info(f"create bucket {self._bucket} successfully")
        else:
            logger.info(f"bucket {self._bucket} exists")

    def delete_bucket(self) -> None:
        exist, bucket = self.__check_bucket()
        if exist:
            try:
                bucket.objects.all().delete()
                bucket.delete()
            except Exception as e:
                print_excp(e)
                logger.info(f"delete bucket {self._bucket} failed")
            else:
                logger.info(f"delete bucket {self._bucket} successfully")
        else:
            logger.info(f"bucket {self._bucket} does not exists")

    def exist(self) -> bool:
        exist, _ = self.__check_bucket()
        return exist

    def get_file(self, file_name: str, path: str) -> None:
        bucket = self._s3.Bucket(self._bucket)
        for obj in bucket.objects.all():
            if obj.key == file_name:
                try:
                    bucket.download_file(file_name, path)
                except Exception as e:
                    print_excp(e)
                    logger.info(f"download file {file_name} failed")
                else:
                    logger.info(f"download file {file_name} successfully")
            else:
                logger.info(f"no file named {file_name} in bucket {self._bucket}")

    def upload_file(self, path: any, file_name: str = None) -> str:
        file_url = ""
        try:
            if file_name is None:
                file_name = path.split('/')[-1]

            extra_args = {}
            if file_name.endswith(".jpg"):
                extra_args =  {"ContentType": "image/jpg"}

            if type(path) == str:
                self._s3.Object(self._bucket, file_name).upload_file(
                    path, ExtraArgs=extra_args)
            elif type(path) == bytes:
                self._s3.Object(self._bucket, file_name).put(Body=path)
        except Exception as e:
            print_excp(e)
            logger.info(f"upload file {file_name} failed")
        else:
            signature = quote(CryptoUtil.hash_sign(self._bucket, file_name, self._secret_key))
            file_url_base = os.path.join(self._s3_base_url, self._bucket, file_name)
            queries = "?Signature=%s&AWSAccessKeyId=%s&Expires=2147483647" % (signature, self._access_key)
            file_url = file_url_base + queries
            logger.info(f"file {file_name} has been uploaded to s3 and the url of file is {file_url}")
        finally:
            return file_url
