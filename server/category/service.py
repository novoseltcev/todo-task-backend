from flask import make_response

from .repository import CategoryRepository
from .schema import CategorySchema

from server.task import service as t_svc


category_rep = CategoryRepository()


@category_rep.assert_kwargs
def open_category(**kwargs):
    return make_response(t_svc.rerender_page())
    # TODO -- app-session open


def create_category(**kwargs):
    category_rep.insert(**kwargs)
    return make_response(t_svc.rerender_page(), 201)


@category_rep.assert_kwargs
def update_category(**kwargs):
    if kwargs['id'] == 1:
        raise ValueError("ban on changing the main category")
    category_rep.update_name(**kwargs)
    return make_response(t_svc.rerender_page(), 202)


@category_rep.assert_kwargs
def delete_category(**kwargs):
    if kwargs['id'] == 1:
        raise ValueError("ban on delete the main category")

    tasks_by_category = t_svc.task_rep.get_by_foreign(*kwargs)
    for task in tasks_by_category:
        t_svc.task_rep.delete(task.id)

    category_rep.delete(**kwargs)
    return make_response(t_svc.rerender_page(), 202)
