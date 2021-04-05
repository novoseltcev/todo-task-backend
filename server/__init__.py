from os import path

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
import boto3
from flask import Flask
from flask_jwt_extended import JWTManager
from redis import StrictRedis
from flask_cors import CORS

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from server.config import Config
from server.celery import make_celery


engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=False)
sqlalchemy_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = sqlalchemy_session.query_property()


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
jwt_redis_blocklist = StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

cors = CORS(resourses={
    r"/*": {'origins': Config.CORS_ALLOWED_ORIGINS}
})


def make_docs(flask_app):
    spec = APISpec(
        title="Swagger TODOTaskManager",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[FlaskPlugin(), MarshmallowPlugin()])
    return spec


celery = make_celery(app)

from server.errors import handler
from server import jwt_auth
from server.views import *

from server.user import user_blueprint
from server.category import category_blueprint
from server.task import task_blueprint
from server.file import file_blueprint

app.register_blueprint(task_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(file_blueprint)
app.register_blueprint(user_blueprint)

from server import initialize_db

__version__ = "0.7"
