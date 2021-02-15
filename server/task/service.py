# Логика приложения (бизнес и прикладная)
from flask import render_template, session

from .repository import TaskRepository
from .schema import TaskSchema

from server.category import service as c_svc
from server.file import service as f_svc


task_rep = TaskRepository()


def rerender_page():
    if 'current_category' not in session:
        session['current_category'] = 1

    current_category = int(session['current_category'])
    if current_category == 1:
        tasks = task_rep.get()
    else:
        try:
            tasks = task_rep.get_by_foreign(current_category)
        except ValueError as error:
            return error.args[0], 404

    categories = c_svc.category_rep.get()
    files = f_svc.file_rep.get()
    assert (len(categories) != 0)
    return render_template("index.html", tasks=tuple(reversed(tasks)), categories=categories, files=files)


def create_task(title, current_category):
    c_svc.category_rep.assert_exist(current_category)
    task_rep.insert(title, current_category)
    return rerender_page(), 201


def update_title(id_task: int, new_title: str):
    task_rep.assert_exist(id_task)
    task_rep.update_title(id_task, new_title)
    return rerender_page(), 202


def update_status(id_task: int):
    task_rep.assert_exist(id_task)
    task_rep.update_status(id_task)
    return rerender_page(), 202


def update_category(id_task: int, new_category: int):
    task_rep.assert_exist(id_task)
    c_svc.category_rep.assert_exist(new_category)
    task_rep.update_category(id_task, new_category)
    return rerender_page(), 202


def delete_task(id: int):
    task_rep.assert_exist(id)

    files_by_task = f_svc.file_rep.get_by_foreign(id)
    for file in files_by_task:
        print(file, file[0])
        f_svc.file_rep.delete(file[0])

    task_rep.delete(id)
    return rerender_page(), 202
