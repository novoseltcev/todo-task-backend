# Серилазизация данных
from server.category.model import Category
from server.category.schema import CategorySchema


def serialize_category(cat: Category, many=False):
    return CategorySchema(many=many).dump(cat)
