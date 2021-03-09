from server.category.repository import CategoryRepository
from server.category.serializer import serialize_category, CategorySchema
from server.errors.exc import ForbiddenOperation
from server.task.service import TaskRepository


def get_all():
    cat = CategoryRepository.get_all()
    return serialize_category(cat, many=True)


def get_by_name(name: str):
    category = CategoryRepository.get_by_name(name)
    return serialize_category(category)


def create(name: str):
    category = CategoryRepository.insert(name)
    return category.id


def update(schema):
    if schema['id'] == 1:
        raise ForbiddenOperation("ban on changing the main category")
    CategoryRepository.update(schema)


def delete(id: int):
    if id == 1:
        raise ForbiddenOperation("ban on delete the main category")

    tasks_by_category = TaskRepository.get_by_category_id(id)
    for task in tasks_by_category:
        TaskRepository.delete(task.id)

    category = CategoryRepository.delete(id)
    return serialize_category(category)
