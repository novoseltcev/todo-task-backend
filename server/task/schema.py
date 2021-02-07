# Валидация данных, простая сериализация
from server.initialize_db import engine
from sqlalchemy import Table, Column, MetaData, Integer, String, ForeignKey

metadata = MetaData(bind=engine)
tasks = Table('tasks', metadata,
              Column('id', Integer, primary_key=True),
              Column('title', String(25)),
              Column('status', Integer),
              Column('category', Integer, ForeignKey('categories.id'))
              )
