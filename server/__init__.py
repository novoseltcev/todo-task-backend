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

from server.config import Config


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

cors = CORS(resourses={r"/*": {'origins': Config.CORS_ALLOWED_ORIGINS}})

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.backend_result)
celery.conf.task_routes = {
    's3_cloud.*': {'queue': 's3'},
    'email.*': {'queue': 'email'}
}


def create_app():
    flask_app = Flask(__name__)
    flask_app.template_folder = os.path.join('static', 'templates')
    flask_app.config.from_object(Config)

    jwt.init_app(flask_app)
    mail.init_app(flask_app)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    @flask_app.teardown_appcontext
    def shutdown_session(exception=None):
        sqlalchemy_session.remove()

    from server import jwt_auth
    from server.async_tasks import email, s3_cloud

    from server.errors.handler import error_blueprint
    from server.views import view_blueprint
    from server.user import user_blueprint
    from server.category import category_blueprint
    from server.task import task_blueprint
    from server.file import file_blueprint

    flask_app.register_blueprint(error_blueprint)
    flask_app.register_blueprint(view_blueprint)
    flask_app.register_blueprint(task_blueprint)
    flask_app.register_blueprint(category_blueprint)
    flask_app.register_blueprint(file_blueprint)
    flask_app.register_blueprint(user_blueprint)

    from server import initialize_db

    return flask_app


app = create_app()
__version__ = "0.7"
