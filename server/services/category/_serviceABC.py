from abc import ABC, abstractmethod

from .schema import CategorySchema
from .response import CategoryResponse


class CategoryService(ABC):
    @classmethod
    @abstractmethod
    def get(cls, schema: CategorySchema) -> CategoryResponse:
        pass

    @classmethod
    @abstractmethod
    def get_all(cls, schema: CategorySchema) -> CategoryResponse:
        pass

    @classmethod
    @abstractmethod
    def create(cls, schema: CategorySchema) -> CategoryResponse:
        pass

    @classmethod
    @abstractmethod
    def edit_name(cls, schema: CategorySchema) -> CategoryResponse:
        pass

    @classmethod
    @abstractmethod
    def delete(cls, schema: CategorySchema) -> CategoryResponse:
        pass
