# Валидация данных, простая сериализация
from server.initialize_db import engine
from sqlalchemy import Table, MetaData, Column, String, Integer, ForeignKey


metadata = MetaData(bind=engine)
files = Table('files', metadata,
              Column('id', Integer, primary_key=True),
              Column('filename', String),
              Column('path', String),
              Column('task', Integer, ForeignKey('tasks.id'))
              )
