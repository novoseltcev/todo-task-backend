# Логика приложения (бизнес и прикладная)
from server.errors.exc import TaskUnknownId, FileUnknownId, CategoryUnknownId
from server.task.repository import TaskRepository
from server.task.serializer import serialize_task, TaskSchema

from server.category.service import CategoryRepository
from server.file.service import FileRepository


def create(schema):
    CategoryRepository.get_by_id(schema['category_id'])
    task = TaskRepository.insert(schema)
    return task.id


def update(schema: dict):
    TaskRepository.update(schema)


def delete(id: int):
    files_by_task = FileRepository.get_by_task_id(id)
    for file in files_by_task:
        FileRepository.delete(file.id)
    task = TaskRepository.delete(id)
    return serialize_task(task)
