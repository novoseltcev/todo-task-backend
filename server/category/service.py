from .repository import CategoryRepository
from .schema import CategorySchema

from server.task import service as svc


category_rep = CategoryRepository()


def open_category(json):
    schema = CategorySchema(only=('id',)).load(json)
    id = schema['id']

    category_rep.assert_exist(id)
    # TODO -- app-session open
    return svc.rerender_page()


def create_category(json):
    schema = CategorySchema(only=('name',)).load(json)
    name = schema['name']

    category_rep.insert(name)
    return svc.rerender_page(), 201


def update_category(json):
    schema = CategorySchema(only=('id', 'name')).load(json)
    id = schema['id']
    source_name = schema['name']

    category_rep.assert_exist(id)
    if id == 1:
        raise ValueError("ban on changing the main category")
    category_rep.update_name(id, source_name)
    return svc.rerender_page(), 202


def delete_category(json):
    schema = CategorySchema(only=('id',)).load(json)
    id = schema['id']

    category_rep.assert_exist(id)
    if id == 1:
        raise ValueError("ban on delete the main category")

    tasks_by_category = svc.task_rep.get_by_foreign(id)
    for task in tasks_by_category:
        svc.task_rep.delete(task.id)

    category_rep.delete(id)
    return svc.rerender_page(), 202
