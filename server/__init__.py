import os

import boto3
from celery import Celery
from flask import Flask
from flask_jwt_extended import JWTManager
from redis import StrictRedis
from flask_cors import CORS
from flask_mail import Mail

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from server.config import BaseConfig, DevConfig  # , ProdConfig
from server.routes import create_routes


Config = DevConfig
cors = CORS(resourses={r"/*": {'origins': BaseConfig.CORS_ALLOWED_ORIGINS}})

engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=False)
sqlalchemy_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = sqlalchemy_session.query_property()

aws_session = boto3.Session(
    aws_access_key_id=Config.AWS_ACCESS_KEY,
    aws_secret_access_key=Config.AWS_SECRET_KEY)
s3 = aws_session.resource('s3')
s3_bucket = s3.Bucket(Config.AWS_BUCKET_NAME)

jwt = JWTManager()
jwt_redis_blocklist = StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

mail = Mail()
mail_redis_tokenlist = StrictRedis(host="localhost", port=6379, db=3, decode_responses=True)

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.backend_result)
celery.conf.task_routes = {
    's3_cloud.*': {'queue': 's3'},
    'email.*': {'queue': 'email'}
}


def create_app(cfg):
    from server import jwt_auth

    flask_app = Flask(__name__)
    flask_app.template_folder = os.path.join('static', 'templates')
    flask_app.config.from_object(cfg)
    jwt.init_app(flask_app)
    create_routes(flask_app)
    if cfg == DevConfig:
        from server import initialize_db

    mail.init_app(flask_app)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    from server import async_tasks

    @flask_app.teardown_appcontext
    def shutdown_session(exception=None):
        sqlalchemy_session.remove()

    return flask_app


app = create_app(DevConfig)
__version__ = "0.7"
