from server.category.repository import CategoryRepository
from server.category.serializer import serialize_category, CategorySchema
from server.task import service as task_service


def get(id_user, id):
    cat = CategoryRepository.get_by_id(id_user, id)
    return serialize_category(cat)


def get_all(id_user: int):
    cat = CategoryRepository.get_by_user_id(id_user)
    return serialize_category(cat, many=True)


def create(id_user: int, name: str):
    category = CategoryRepository.insert(id_user, name)
    return category.id


def update(id_user, schema):
    CategoryRepository.update(id_user, schema)


def delete(id_user: int, id: int):
    category = CategoryRepository.delete(id_user, id)
    tasks_by_category = category.tasks
    for task in tasks_by_category:
        task_service.delete(id_user, task.id)

    return serialize_category(category)
