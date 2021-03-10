from datetime import timedelta
from os import path, environ

from dotenv import load_dotenv

from flask import Flask
from flask_jwt_extended import JWTManager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from server.config import Config

load_dotenv('.env')
config = Config()
app = Flask(__name__)
app.template_folder = path.join('static', 'templates')
app.config.from_object(config)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=15)
app.config['SQLALCHEMY_DATABASE_URL'] = environ.get('DATABASE_URL')

jwt = JWTManager(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URL'], echo=False)

DB_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = DB_session.query_property()


from server.user import user_blueprint
from server.category import category_blueprint
from server.task import task_blueprint
from server.file import file_blueprint


app.register_blueprint(task_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(file_blueprint)
app.register_blueprint(user_blueprint)


from server import initialize_db

from server.errors import handler
from server.index import index


__version__ = "0.5"
