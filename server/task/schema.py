# Валидация данных, простая сериализация
from server.initialize_db import metadata, engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey

tasks = Table('tasks', metadata,
              Column('id', Integer, primary_key=True),
              Column('title', String(25)),
              Column('status', Integer),
              Column('category', Integer, ForeignKey('categories.id'))
              )
metadata.create_all()
