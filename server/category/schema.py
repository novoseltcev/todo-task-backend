# Валидация данных, простая сериализация
from server.category.repository import CategoryRepository
from sqlalchemy import Table, Column, MetaData, Integer, String


def validate_name(name: str):
    category_rep = CategoryRepository()
    if len(category_rep.get_by_name(name)) == 0:
        raise ValueError()

metadata = MetaData()
categories = Table('categories', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(25))
                   )

