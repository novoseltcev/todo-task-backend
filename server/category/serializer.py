# Серилазизация данных
from sqlalchemy.orm import mapper, relationship
from server.category.model import Category
from server.category.schema import categories

from server.task.model import Task
from server.task.repository import tasks

mapper(Category, categories,
       properties={
           'categories': relationship(Task, backref='tasks', order_by=tasks.c.id)
       }
       )
