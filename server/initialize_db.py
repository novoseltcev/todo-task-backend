from os import getcwd, path

from sqlalchemy import create_engine, MetaData


cwd = getcwd()
engine = create_engine('sqlite:///' + path.join(cwd, 'server', 'data', 'task.db'), echo=False)
metadata = MetaData(bind=engine)
