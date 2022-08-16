from .model import Task
from .repository import TaskRepository

from app.rest_lib.services import Service
from app.errors import NoSuchEntityError, ChangeCategoryError
from app.entities.category.service import CategoryService


class TaskService(Service):
    repository: TaskRepository

    def __init__(self, repository: TaskRepository = TaskRepository()):
        super().__init__(repository=repository)
        self.category_service: CategoryService = CategoryService()

    def get_by_pk(self, user_id: int, entity_id: int) -> Task:
        task = self.repository.get_by_pk(
            self.repository.PrimaryKey(
                user_id=user_id,
                id=entity_id
            )
        )
        if not task:
            raise NoSuchEntityError('Задача не существует.')

        return task

    def create(self, user_id: int, data: dict) -> Task:
        task = Task(**data, user_id=user_id)
        self.repository.insert(task)
        return task

    def edit(self, user_id: int, entity_id: int, data: dict) -> None:
        self.repository.update(
            data=data,
            pk=self.repository.PrimaryKey(
                user_id=user_id,
                id=entity_id
            )
        )

    def change_category(self, user_id: int, entity_id: int, category_name: str) -> None:
        next_category = self.category_service.get_by_pk(user_id=user_id, name=category_name)
        if not next_category:
            raise ChangeCategoryError()

        self.repository.update(
            data={'category_name': category_name},
            pk=self.repository.PrimaryKey(
                user_id=user_id,
                id=entity_id
            )
        )

    def delete(self, user_id: int, entity_id: id) -> None:
        self.repository.delete(
            self.repository.PrimaryKey(
                user_id=user_id,
                id=entity_id
            )
        )
