from abc import ABC, abstractmethod

from ..adapter import repository, storage


class AbstractUnitOfWork(ABC):
    categories: repository.AbstractRepository
    storage: storage.AbstractStorage

    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    @abstractmethod
    def commit(self):
        ...

    @abstractmethod
    def rollback(self):
        ...


class ContentUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=...):
        self.session_factory = session_factory

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            for path in self.storage.loaded_paths:
                self.storage.delete(path)

        super().__exit__(exc_type, exc_val, exc_tb)
        self.session.close()

    def __enter__(self):
        self.session = self.session_factory()
        self.categories = repository.Categories(self.session)
        self.storage = storage.S3Storage()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
