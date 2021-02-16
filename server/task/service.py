# Логика приложения (бизнес и прикладная)
from flask import render_template, session, redirect
from flask_apispec import use_kwargs

from .repository import TaskRepository
from .schema import TaskSchema

from server.category import service as c_svc
from server.file import service as f_svc


task_rep = TaskRepository()


def rerender_page():
    if 'current_category' not in session:
        session['current_category'] = 1

    current_category = int(session['current_category'])
    data = c_svc.CategorySchema(many=True).dump(c_svc.category_rep.get())

    from pprint import pprint
    pprint(data)

    assert (len(data) != 0)
    return render_template("index.html", data=data, current_category=current_category)


def create_task(current_category, **kwargs):
    title = kwargs['title']
    c_svc.category_rep.assert_exist(current_category)
    task_rep.insert(title, current_category)
    return redirect('/', 201)


def update_title(data):
    schema = TaskSchema(only=('id', 'title')).load(data)
    id = schema['id']
    task_rep.assert_exist(id)

    new_title = schema['title']
    task_rep.update_title(id, new_title)
    return redirect('/', 202)


def update_status(**kwargs):
    id = kwargs['id']
    task_rep.assert_exist(id)

    task_rep.update_status(id)
    return redirect('/', 202)


# @task_rep.assert_exist
def update_category(**kwargs):
    id = kwargs['id']
    new_category = kwargs['category']
    task_rep.assert_exist(id)

    c_svc.category_rep.assert_exist(new_category)
    task_rep.update_category(id, new_category)
    return redirect('/', 202)


def delete_task(**kwargs):
    id = kwargs['id']
    task_rep.assert_exist(id)

    files_by_task = f_svc.file_rep.get_by_foreign(id)
    for file in files_by_task:
        print(file, file.id)
        f_svc.file_rep.delete(file.id)

    task_rep.delete(id)
    return redirect('/', 202)
