# Логика приложения (бизнес и прикладная)
from flask import session

from .repository import TaskRepository

from server.category import service as c_svc
from server.file import service as f_svc


task_rep = TaskRepository()


def create_task(**kwargs):
    c_svc.category_rep.assert_exist(kwargs['category'])
    task_rep.insert(**kwargs)


@task_rep.assert_kwargs
def update_title(**kwargs):
    task_rep.update_title(**kwargs)


@task_rep.assert_kwargs
def update_status(**kwargs):
    task_rep.update_status(**kwargs)


@task_rep.assert_kwargs
def update_category(**kwargs):
    c_svc.category_rep.assert_exist(kwargs['category'])
    task_rep.update_category(**kwargs)


@task_rep.assert_kwargs
def delete_task(**kwargs):
    files_by_task = f_svc.file_rep.get_by_foreign(*kwargs)
    for file in files_by_task:
        f_svc.file_rep.delete(file.id)

    task_rep.delete(**kwargs)
