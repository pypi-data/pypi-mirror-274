'''
@File    :   aios3.py
@Time    :   2022/07/11 18:20:42
@Author  :   susufqx
@Version :   1.0
@Contact :   jiangsulirui@gmail.com
'''


import aioboto3
from .log import logger


REGION_NAME = 'str'
S3_ACCESS_KEY_ID = ''
S3_SECRET_ACCESS_KEY = ''
S3_BASE_URL = 'https://s3.harix.iamidata.com'


# def connect(f):
#     async def g(self, *args, **kwargs):
#         s3 = aioboto3.resource('s3',
#                                region_name=REGION_NAME,
#                                S3_ACCESS_KEY_ID=S3_ACCESS_KEY_ID,
#                                S3_SECRET_ACCESS_KEY=S3_SECRET_ACCESS_KEY)
#         res = await f(self, s3, *args, **kwargs)

#         try:
#             await s3.close()
#         except Exception as err:
#             logger.debug(f'[UPLOAD] {err}')
#         finally:
#             return res

#     return g


class aioS3:
    # '''
    # config = dict(
    #     bucket = xxx,

    # )
    # '''

    # def __init__(self, config: dict):
    #     self._bucket = config.get("bucket")

    # @connect
    # def bucket_exist(self):
    #     pass

    # @connect
    # def get(self):
    #     pass

    # @connect
    # def upload(self):
    #     pass
    pass
