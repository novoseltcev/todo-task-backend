import os

from . import engine, Base

from .user import model
from .category import model
from .task import model
from .file import model

cwd = os.getcwd()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

with open(os.path.join(cwd, 'server', 'inserts.sql')) as inserts_file:
    for insert in inserts_file:
        engine.execute(insert)
