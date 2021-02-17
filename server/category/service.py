from .repository import CategoryRepository
from .serializer import serialize_category, CategorySchema

from server.task import service as t_svc


category_rep = CategoryRepository()


def get_categories():
    cat = category_rep.get()
    return {'data': serialize_category(cat, many=True)}


def get_category(**kwargs):
    cat = category_rep._get_by(**kwargs)
    return serialize_category(cat)


@category_rep.assert_kwargs
def open_category(**kwargs):
    pass


def create_category(**kwargs):
    category_rep.insert(**kwargs)


@category_rep.assert_kwargs
def update_category(**kwargs):
    if kwargs['id'] == 1:
        raise ValueError("ban on changing the main category")
    category_rep.update_name(**kwargs)


@category_rep.assert_kwargs
def delete_category(**kwargs):
    if kwargs['id'] == 1:
        raise ValueError("ban on delete the main category")

    tasks_by_category = t_svc.task_rep.get_by_foreign(*kwargs)
    for task in tasks_by_category:
        t_svc.task_rep.delete(task.id)

    category_rep.delete(**kwargs)
