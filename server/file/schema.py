# Валидация данных, простая сериализация
from sqlalchemy import Table, MetaData, Column, String, Integer, ForeignKey

from server.initialize_db import engine, metadata


files = Table('files', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('path', String, unique=True),
              Column('task', Integer, ForeignKey('tasks.id'))
              )
metadata.create_all()
