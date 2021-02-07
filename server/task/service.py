# Логика приложения (бизнес и прикладная)
from flask import render_template, session
from server.task.repository import TaskRepository
from server.task.serializer import Task, engine
from server.category.service import category_rep
from server.file.service import file_rep


task_rep = TaskRepository(engine, Task)


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

    categories = category_rep.get()
    files = file_rep.get()
    assert (len(categories) != 0)
    return render_template("index.html", tasks=tasks, categories=categories, files=files)


def create_task(title, current_category):
    category_rep.assert_exist(current_category)
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
    category_rep.assert_exist(new_category)
    task_rep.update_category(id_task, new_category)
    return rerender_page(), 202


def delete_task(id: int):
    task_rep.assert_exist(id)

    files_by_task = file_rep.get_by_foreign(id)
    for file in files_by_task:
        print(file, file[0])
        file_rep.delete(file[0])

    task_rep.delete(id)
    return rerender_page(), 202
