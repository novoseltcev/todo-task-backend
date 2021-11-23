from abc import ABC, abstractmethod

from .response import TaskResponse, TaskSchema


class TaskService(ABC):
    @classmethod
    @abstractmethod
    def get(cls, schema: TaskSchema) -> TaskResponse:
        pass

    @classmethod
    @abstractmethod
    def get_all(cls, schema: TaskSchema) -> TaskResponse:
        pass

    @classmethod
    @abstractmethod
    def create(cls, schema: TaskSchema) -> TaskResponse:
        pass

    @classmethod
    @abstractmethod
    def edit_title(cls, schema: TaskSchema) -> TaskResponse:
        pass

    @classmethod
    @abstractmethod
    def change_status(cls, schema: TaskSchema) -> TaskResponse:
        pass

    @classmethod
    @abstractmethod
    def change_category(cls, schema: TaskSchema) -> TaskResponse:
        pass

    @classmethod
    @abstractmethod
    def delete(cls, schema: TaskSchema) -> TaskResponse:
        pass
