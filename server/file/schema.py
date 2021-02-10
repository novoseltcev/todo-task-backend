# Валидация данных, простая сериализация
from server.initialize_db import engine, metadata
from sqlalchemy import Table, MetaData, Column, String, Integer, ForeignKey


files = Table('files', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('path', String),
              Column('task', Integer, ForeignKey('tasks.id'))
              )
metadata.create_all()
