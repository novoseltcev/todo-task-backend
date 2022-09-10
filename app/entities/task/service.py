from .repository import TaskRepository, Task, PK

from app.rest_lib.services import Service
from app.errors import NoSuchEntityError, ChangeCategoryError, LogicError
from app.entities.category.service import CategoryService


class TaskService(Service):
    repository: TaskRepository

    def __init__(self, repository: TaskRepository = TaskRepository()):
        super().__init__(repository=repository)
        self.category_service: CategoryService = CategoryService()

    def get_by_pk(self, user_id: int, entity_id: int) -> Task:
        task = self.repository.get_by_pk(PK(user_id=user_id, id=entity_id))
        if not task:
            raise NoSuchEntityError('Задача не существует.')

        return task

    def create(self, user_id: int, data: dict) -> Task.id:
        try:
            self.category_service.get_by_pk(user_id=user_id, entity_id=data['category_id'])
        except NoSuchEntityError as e:
            raise LogicError('Привязка к несуществующей категории') from e

        task = Task(**data, user_id=user_id)
        self.repository.insert(task)
        return task.id

    def edit(self, user_id: int, entity_id: int, data: dict) -> None:
        self.repository.update(
            data=data,
            pk=PK(user_id=user_id, id=entity_id)
        )

    def change_category(self, user_id: int, entity_id: int, category_id: int) -> None:
        try:
            self.category_service.get_by_pk(user_id=user_id, entity_id=category_id)
        except NoSuchEntityError as e:
            raise ChangeCategoryError() from e

        self.repository.update(
            data=dict(category_id=category_id),
            pk=PK(user_id=user_id, id=entity_id)
        )

    def delete(self, user_id: int, entity_id: id) -> None:
        self.repository.delete(PK(user_id=user_id, id=entity_id))
