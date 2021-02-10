# Валидация данных, простая сериализация
from sqlalchemy import Table, Column, Integer, String, UniqueConstraint

from server.initialize_db import metadata, engine


categories = Table('categories', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(25), unique=True)
                   )
metadata.create_all()
