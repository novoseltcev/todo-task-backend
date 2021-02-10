# Серилазизация данных
from sqlalchemy.orm import mapper, relationship
from server.task.model import Task
from server.task.schema import tasks, engine

# from server.file.schema import files
# from server.file.model import File


mapper(Task, tasks)
       # properties={
       #     'files': relationship(File, backref='files', order_by=files.c.id)  # TODO - check docs
       # })
