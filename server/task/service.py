# Логика приложения (бизнес и прикладная)
from server.errors.exc import TaskUnknownId, FileUnknownId, CategoryUnknownId
from server.task.repository import TaskRepository
from server.task.serializer import serialize_task, TaskSchema

from server.category.service import CategoryRepository
from server.file.service import FileRepository


def create(id_user, schema):
    CategoryRepository.get_by_id(id_user, schema['id_category'])
    task = TaskRepository.insert(id_user, schema)
    return task.id


def update(id_user, schema: dict):
    TaskRepository.update(id_user, schema)


def delete(id_user: int, id: int):
    files_by_task = FileRepository.get_by_task_id(id_user, id)
    for file in files_by_task:
        FileRepository.delete(id_user, file.id)
    task = TaskRepository.delete(id_user, id)
    return serialize_task(task)
