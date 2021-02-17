# Серилазизация данных
from .model import Category
from .schema import CategorySchema


def serialize_category(cat: Category, many=False):
    return CategorySchema(many=many).dump(cat)
