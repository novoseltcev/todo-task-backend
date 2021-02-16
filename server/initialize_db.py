from os import getcwd, path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


cwd = getcwd()
DB_config = {'task_title_len': 25, 'category_name_len': 15, 'filename_len': 228, 'files_dir_len': 0,
             'UPLOAD_FOLDER': path.join('data', 'files'), 'ROOT': 'server'}

engine = create_engine('sqlite:///' + path.join(cwd, DB_config['ROOT'], 'data', 'task.db'),
                       echo=False)
DB_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = DB_session.query_property()

