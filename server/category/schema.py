# Валидация данных, простая сериализация
from server.initialize_db import engine
from sqlalchemy import Table, Column, MetaData, Integer, String, UniqueConstraint


metadata = MetaData(bind=engine)
categories = Table('categories', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(25))
                   )
