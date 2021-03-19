from server.category.repository import CategoryRepository
from server.category.serializer import serialize_category, CategorySchema
from server.errors.exc import ForbiddenOperation
from server.task.service import TaskRepository


def get_all(id_user: int):
    cat = CategoryRepository.get_by_user_id(id_user)
    return serialize_category(cat, many=True)


def create(id_user: int, name: str):
    category = CategoryRepository.insert(id_user, name)
    return category.id


def update(id_user, schema):
    CategoryRepository.update(id_user, schema)


def delete(id_user: int, id: int):
    if id == 1:
        raise ForbiddenOperation("ban on delete the main category")

    category = CategoryRepository.delete(id_user, id)
    tasks_by_category = TaskRepository.get_by_category_id(id_user, id)
    for task in tasks_by_category:
        TaskRepository.delete(id_user, task.id)

    return serialize_category(category)
