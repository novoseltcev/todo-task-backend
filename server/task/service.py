from server.task.repository import TaskRepository
from server.task.serializer import serialize_task, TaskSchema

from server.category import service as category_service


def get(id_user, id):
    task = TaskRepository.get_by_id(id_user, id)
    return serialize_task(task)


def create(id_user, schema):
    category_service.get(id_user, schema['id_category'])
    task = TaskRepository.insert(id_user, schema)
    return task.id


def update(id_user, schema: dict):
    TaskRepository.update(id_user, schema)


def delete(id_user: int, id: int):
    task = TaskRepository.delete(id_user, id)
    return serialize_task(task)
