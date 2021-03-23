import os
from os import path

import boto3
from flask import Flask
from flask_jwt_extended import JWTManager
from redis import StrictRedis
from celery import Celery
from flask_cors import CORS

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from server.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=False)

DB_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = DB_session.query_property()

jwt_redis_blocklist = StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

aws_session = boto3.Session(
    aws_access_key_id=Config.AWS_ACCESS_KEY,
    aws_secret_access_key=Config.AWS_SECRET_KEY
)
s3 = aws_session.resource('s3')
s3_bucket = s3.Bucket(Config.AWS_BUCKET_NAME)

app = Flask(__name__)
app.template_folder = path.join('static', 'templates')
app.config.from_object(Config)

jwt = JWTManager(app)

cors = CORS(resourses={
    r"/*": {'origins': Config.CORS_ALLOWED_ORIGINS}
})


def make_celery(flask_app):
    celery_app = Celery(flask_app.name,
                        broker=flask_app.config['CELERY_BROKER_URL'],
                        backend=Config.backend_result
                        )
    celery_app.conf.update(flask_app.config)

    celery_app.task_routes = {
        's3_cloud.*': {'queue': 's3'},
        'email.*': {'queue': 'email'}
    }

    task_base = celery_app.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


celery = make_celery(app)

from server.user import user_blueprint
from server.category import category_blueprint
from server.task import task_blueprint
from server.file import file_blueprint

app.register_blueprint(task_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(file_blueprint)
app.register_blueprint(user_blueprint)

from server.views import *
from server import initialize_db
from server.errors import handler
from server import jwt_auth

__version__ = "0.7"
