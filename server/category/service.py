from flask import redirect

from .repository import CategoryRepository
from .schema import CategorySchema

from server.task import service as svc


category_rep = CategoryRepository()


def open_category(**kwargs):
    id = kwargs['id']
    category_rep.assert_exist(id)

    # TODO -- app-session open
    return redirect('/', 200)


def create_category(**kwargs):
    name = kwargs['name']

    category_rep.insert(name)
    return redirect('/', 201)


def update_category(**kwargs):
    id = kwargs['id']
    category_rep.assert_exist(id)

    source_name = kwargs['name']
    if id == 1:
        raise ValueError("ban on changing the main category")
    category_rep.update_name(id, source_name)
    return redirect('/', 202)


def delete_category(**kwargs):
    id = kwargs['id']

    category_rep.assert_exist(id)
    if id == 1:
        raise ValueError("ban on delete the main category")

    tasks_by_category = svc.task_rep.get_by_foreign(id)
    for task in tasks_by_category:
        svc.task_rep.delete(task.id)

    category_rep.delete(id)
    return redirect('/', 202)
