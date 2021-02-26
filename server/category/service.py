from .repository import CategoryRepository
from .serializer import serialize_category, CategorySchema

category_repository = CategoryRepository()
from server.task.service import task_repository


def get_all():
    cat = category_repository.get_all()
    return serialize_category(cat, many=True)


def get_one(id: int):
    category = category_repository.get_by_primary(id)
    return serialize_category(category)


def get_by_name(name: str):
    category = category_repository.get_by_name(name)
    return serialize_category(category)


def create(name: str):
    category_repository.insert(name)


@category_repository.assert_id
def update(id: int, name: str):
    if id == 1:
        raise ValueError("ban on changing the main category")
    category_repository.update(id, name)


@category_repository.assert_id
def delete(id: int):
    if id == 1:
        raise ValueError("ban on delete the main category")

    tasks_by_category = task_repository.get_by_foreign(id)
    for task in tasks_by_category:
        task_repository.delete(task.id)

    category_repository.delete(id)
