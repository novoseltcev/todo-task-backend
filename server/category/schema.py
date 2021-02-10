# Валидация данных, простая сериализация
from server.initialize_db import metadata, engine
from sqlalchemy import Table, Column, Integer, String, UniqueConstraint

categories = Table('categories', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(25))
                   )
metadata.create_all()
