# Серилазизация данных
from sqlalchemy.orm import mapper
from server.file.model import File
from server.file.repository import files

mapper(File, files)
