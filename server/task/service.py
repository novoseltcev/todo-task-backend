# Логика приложения (бизнес и прикладная)
from flask import render_template, session, make_response

from .repository import TaskRepository

from server.category import service as c_svc
from server.file import service as f_svc


task_rep = TaskRepository()


def rerender_page():
    if 'current_category' not in session:
        session['current_category'] = 1

    current_category = int(session['current_category'])
    data = c_svc.CategorySchema(many=True).dump(c_svc.category_rep.get())
    assert (len(data) != 0)
    return render_template("index.html", data=data, current_category=current_category)


def create_task(current_category, **kwargs):
    title = kwargs['title']
    c_svc.category_rep.assert_exist(current_category)
    task_rep.insert(title, current_category)
    return make_response(rerender_page(), 201)


@task_rep.assert_kwargs
def update_title(**kwargs):
    task_rep.update_title(**kwargs)
    return make_response(rerender_page(), 202)


@task_rep.assert_kwargs
def update_status(**kwargs):
    task_rep.update_status(**kwargs)
    return make_response(rerender_page(), 202)


@task_rep.assert_kwargs
def update_category(**kwargs):
    c_svc.category_rep.assert_exist(kwargs['category'])
    task_rep.update_category(**kwargs)
    return make_response(rerender_page(), 202)


@task_rep.assert_kwargs
def delete_task(**kwargs):
    files_by_task = f_svc.file_rep.get_by_foreign(*kwargs)
    for file in files_by_task:
        f_svc.file_rep.delete(file.id)

    task_rep.delete(**kwargs)
    return make_response(rerender_page(), 202)
