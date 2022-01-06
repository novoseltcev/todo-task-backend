from server.user import *
from server.folder import *
from server.task import *
from server.file import *

# import os
#
# import boto3
# from celery import Celery
# from flask import Flask
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# from flask_mail import Mail
# from redis import StrictRedis
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, scoped_session
#
# from server.config import BaseConfig, DevConfig  # , ProdConfig
# from server.controllers import api_blueprint
#
# Config = DevConfig
# cors = CORS(resourses={r"/*": {'origins': BaseConfig.CORS_ALLOWED_ORIGINS}})
#
# engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=False)
# sqlalchemy_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# Base = declarative_base()
# Base.query = sqlalchemy_session.query_property()
#
# aws_session = boto3.Session(
#     aws_access_key_id=Config.AWS_ACCESS_KEY,
#     aws_secret_access_key=Config.AWS_SECRET_KEY)
# s3 = aws_session.resource('s3')
# s3_bucket = s3.Bucket(Config.AWS_BUCKET_NAME)
#
# jwt = JWTManager()
# jwt_redis_blocklist = StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
#
# mail = Mail()
# mail_redis_tokenlist = StrictRedis(host="localhost", port=6379, db=3, decode_responses=True)
#
# celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.backend_result)
# celery.conf.task_routes = {
#     's3_cloud.*': {'queue': 's3'},
#     'mail.*': {'queue': 'mail'}
# }
#
#
# def create_app(cfg):
#     from server import jwt_auth
#
#     flask_app = Flask(__name__)
#     flask_app.template_folder = os.path.join('static', 'templates')
#     flask_app.config.from_object(cfg)
#     cors.init_app(flask_app)
#     jwt.init_app(flask_app)
#     flask_app.register_blueprint(api_blueprint)
#     if cfg == DevConfig:
#         from server import initialize_db
#
#     mail.init_app(flask_app)
#     TaskBase = celery.Task
#
#     class ContextTask(TaskBase):
#         abstract = True
#
#         def __call__(self, *args, **kwargs):
#             with flask_app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#
#     celery.Task = ContextTask
#     from server import async_tasks
#
#     @flask_app.teardown_appcontext
#     def shutdown_session(exception=None):
#         sqlalchemy_session.remove()
#
#     return flask_app
#
#
# app = create_app(DevConfig)
# __version__ = "1.0"
