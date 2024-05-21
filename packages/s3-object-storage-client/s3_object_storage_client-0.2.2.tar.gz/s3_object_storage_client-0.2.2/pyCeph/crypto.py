'''
@File    :   crypto.py
@Time    :   2022/07/14 15:13:18
@Author  :   susufqx
@Version :   1.0
@Contact :   jiangsulirui@gmail.com
'''


import hmac
import base64
from hashlib import sha1


class CryptoUtil:

    @staticmethod
    def hash_sign(name, path, s_key, expire_ttl="2147483647"):
        str_1 = "GET\n\n\n%s\n/%s/%s" % (expire_ttl, name, path)
        hmac_code = hmac.new(s_key.encode(), str_1.encode(), sha1)
        return base64.b64encode(hmac_code.digest()).decode()
