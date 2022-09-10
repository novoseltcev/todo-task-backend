from datetime import timedelta
from distutils.util import strtobool
from os import environ


class __DBConfig:
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = strtobool(environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'))


class __AWSConfig:
    AWS_ACCESS_KEY = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = environ.get('AWS_SECRET_KEY')
    AWS_BUCKET_NAME = environ.get('AWS_BUCKET_NAME')


class __JWTConfig:
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)


class __BROKERConfig:
    CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL')
    BACKEND_RESULT = environ.get('CELERY_RESULT_BACKEND')


class Config(__DBConfig, __JWTConfig, __BROKERConfig, __AWSConfig):
    DEBUG: bool = strtobool(environ.get('DEBUG', default='False'))
    SECRET_KEY: str = environ.get('SECRET_KEY')
    AUTH_DISABLE: bool = strtobool(environ.get('AUTH_DISABLE', 'False'))

    TMP_FILE_PATH: str = environ.get('TMP_FILE_PATH')
    PERMANENT_FILE_PATH: str = environ.get('PERMANENT_FILE_PATH')


config = Config()
