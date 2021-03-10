from server.category.repository import CategoryRepository
from server.category.serializer import serialize_category, CategorySchema
from server.errors.exc import ForbiddenOperation
from server.task.service import TaskRepository


def get_all(user_id):
    cat = CategoryRepository.get_by_user_id(user_id)
    return serialize_category(cat, many=True)


def create(name: str, user_id: int):
    category = CategoryRepository.insert(name, user_id)
    return category.id


def update(schema, user_id):
    if schema['id'] == 1:
        raise ForbiddenOperation("ban on changing the main category")
    CategoryRepository.update(schema, user_id)


def delete(id: int, user_id: int):
    if id == 1:
        raise ForbiddenOperation("ban on delete the main category")

    category = CategoryRepository.delete(id, user_id)
    tasks_by_category = TaskRepository.get_by_category_id(id)
    for task in tasks_by_category:
        TaskRepository.delete(task.id)

    return serialize_category(category)
