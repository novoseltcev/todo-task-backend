from abc import ABC, abstractmethod

from ..domain import model


class AbstractRepository(ABC):
    @abstractmethod
    def get(self, category_ref: str) -> model.Category:
        """Load a Category by himself reference from the system."""

    @abstractmethod
    def get_by_task(self, task_ref: str) -> model.Category:
        """Load a Category by a reference to a linked Task from the system."""

    @abstractmethod
    def get_by_file(self, file_ref: str) -> model.Category:
        """Load a Category by a reference to a linked File from the system."""

    @abstractmethod
    def add(self, category: model.Category) -> None:
        """Add of the created Category in the system."""

    @abstractmethod
    def delete(self, category: model.Category) -> None:
        """Delete a Category from the system."""


class Categories(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get(self, ref: str) -> model.Category:
        return self.session.query(model.Category).filer_by(id=ref).first()

    def get_by_task(self, ref: str) -> model.Category:  # TODO
        return self.session.query(model.Category) \
            .join(model.Task) \
            .filer(id=ref).first()

    def get_by_file(self, ref: str) -> model.Category:  # TODO
        return self.session.query(model.Category) \
            .join(model.Task).join(model.File) \
            .filter(id=ref).first()

    def add(self, category: model.Category) -> None:
        self.session.add(category)

    def delete(self, category: model.Category) -> None:
        self.session.delete(category)
