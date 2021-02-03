# Серилазизация данных
from sqlalchemy.orm import mapper, relationship
from server.task.model import Task
from server.file.repository import files

from server.file.model import File
from server.task.repository import tasks


mapper(Task, tasks,
       properties={
           'files': relationship(File, backref='files', order_by=files.c.id)
       })
