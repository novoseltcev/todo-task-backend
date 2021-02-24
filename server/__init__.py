import os

from flask import Flask
from flask_login import LoginManager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from .config import Config


config = Config()
app = Flask(__name__)
app.template_folder = os.path.join('static', 'templates')
app.config.from_object(config)

login_manager = LoginManager(app)

engine = create_engine('sqlite:///' + os.path.join(os.getcwd(), app.config['ROOT'], 'data', 'task.db'),
                       echo=False)
DB_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = DB_session.query_property()


from . import initialize_db

from .errors import handler
from .index import index

from .category import category_blueprint
from .task import task_blueprint
from .file import file_blueprint


app.register_blueprint(task_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(file_blueprint)

__version__ = "0.3"
