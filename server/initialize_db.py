from os import getcwd, path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from .config import Config

cwd = getcwd()

config = Config()
engine = create_engine('sqlite:///' + path.join(cwd, config.ROOT, 'data', 'task.db'),
                       echo=False)
DB_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = DB_session.query_property()

from .category import model
from .task import model
from .file import model

Base.metadata.create_all(bind=engine)
