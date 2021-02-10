# Серилазизация данных
from sqlalchemy.orm import mapper

from server.file.model import File
from server.file.schema import files, engine


mapper(File, files)
