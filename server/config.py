from os import environ
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv('.env')


class Config:
    USE_PERMANENT_SESSION = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=5)

    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)

    SECRET_KEY = environ.get('SECRET_KEY')
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URL = environ.get('DATABASE_URL')
    CELERY_BROKER_URL = environ.get('CELERY_BROKER_URL')
    result_backend = environ.get('CELERY_RESULT_BACKEND ')

    AWS_ACCESS_KEY = environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = environ.get('AWS_SECRET_KEY')
    AWS_BUCKET_NAME = environ.get('AWS_BUCKET_NAME')

    task_title_len = 25
    category_name_len = 15
    filename_len = 228
    files_dir_len = 0

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'flask@example.com'
