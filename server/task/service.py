# Логика приложения (бизнес и прикладная)
from server.locale import rerender_page
from server.task.model import Task
from server.task.repository import task_rep
from server.task import serializer


def create_task(title, current_category):
    task_rep.insert(title, current_category)
    return rerender_page(), 201


def update_status(id_task: int, status: int):
    task_rep.assert_exist(id_task)
    task_rep.update_status(id_task, status)
    return rerender_page(), 202


def update_category(id_task: int, new_category: int):
    task_rep.assert_exist(id_task)
    task_rep.update_category(id_task, new_category)
    return rerender_page(), 202


def delete_task(id_task: int):
    task_rep.assert_exist(id_task)
    task_rep.delete(id_task)
    return rerender_page(), 202
