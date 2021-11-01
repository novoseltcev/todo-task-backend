from server.api.category.model import Category
from server.api.category.schema import CategorySchema


def serialize_category(cat: Category, many=False):
    return CategorySchema(many=many).dump(cat)
