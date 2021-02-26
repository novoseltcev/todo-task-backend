# Логика приложения (бизнес и прикладная)
from .repository import TaskRepository
from .serializer import serialize_task

task_repository = TaskRepository()
from server.category.service import category_repository
from server.file.service import file_repository


@task_repository.assert_id
def get_one(id: int):
    task = task_repository.get_by_primary(id)
    return serialize_task(task)


@category_repository.assert_id('category')
def create(title: str, category: int):
    task_repository.insert(title, category)


@category_repository.assert_id('category')
@task_repository.assert_id
def update(id: int, title: str, status: int, category: int):
    task_repository.update(id, title, status, category)


@task_repository.assert_id
def delete(id: int):
    files_by_task = file_repository.get_by_foreign(id)
    for file in files_by_task:
        file_repository.delete(file.id)

    task_repository.delete(id)
