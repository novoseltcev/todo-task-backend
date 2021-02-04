from server.category.repository import CategoryRepository
from server.category.serializer import Category, engine
from server.task import service as svc


category_rep = CategoryRepository(engine, Category)


def open_category(id_category: int):
    category_rep.assert_exist(id_category)
    return svc.rerender_page()


def create_category(name):
    category_rep.insert(name)
    return svc.rerender_page(), 201


def update_category(id_category: int, source_name: str):
    category_rep.assert_exist(id_category)
    if id_category == 1:
        raise ValueError("ban on changing the main category")
    category_rep.update_name(id_category, source_name)
    return svc.rerender_page(), 202


def delete_category(id_category: int):
    category_rep.assert_exist(id_category)
    # category_rep.get_by_primary(id_category)
    category_rep.delete(id_category)
    return svc.rerender_page(), 202
