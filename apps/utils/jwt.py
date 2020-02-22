import functools

import jwt
from dynaconf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as serial
from apps.utils import logger
from apps.utils import exceptions


class JwtSerial:
    # 对称加密解密
    def __init__(self):
        jwt_env = settings.from_env('jwt')
        self.serial = serial(secret_key=jwt_env['secret-key'],
                             salt=jwt_env['salt'],
                             expires_in=jwt_env['expires'])

    def dumps(self, data):
        return self.serial.dumps(data)

    def loads(self, token):
        try:
            res = self.serial.loads(token)
        except Exception as ex:
            logger.error(ex)
            raise exceptions.TokenBad(info=ex)
        return res


class JwtRSA:
    # 非对称加密解密
    def __init__(self):
        jwt_env = settings.from_env('jwt')
        with open(jwt_env['private_key']) as f:
            self.private_key = f.read()
        with open(jwt_env['public_key']) as f:
            self.public_key = f.read()

    def dumps(self, data):
        return jwt.encode(data, self.private_key, algorithm='RS256')

    def loads(self, token):
        try:
            res = jwt.decode(token, self.public_key, algorithms='RS256')
        except Exception as ex:
            logger.error(ex)
            raise exceptions.TokenBad(info=ex)
        return res
