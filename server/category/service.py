from server.locale import rerender_page
from server.category.model import Category
from server.category.repository import category_rep
from server.category import serializer
from server.category import schema


def open_category(id_category: int):
    category_rep.assert_exist(id_category)
    return rerender_page()


def create_category(name):
    schema.validate_name(name)
    category = Category(name)
    return rerender_page(), 201


def update_category(id_category: int, source_name: str):
    category = Category(serializer.by_id(id_category))
    category_rep.assert_exist(id_category)
    if id_category == 1:
        raise ValueError("ban on changing the main category")
    category_rep.update_name(id_category, source_name)
    return rerender_page(), 202


def delete_category(id_category: int):
    category = Category(serializer.by_id(id_category))
    category_rep.assert_exist(id_category)
    category_rep.get_by_primary(id_category)
    category_rep.delete(id_category)
    return rerender_page(), 202
