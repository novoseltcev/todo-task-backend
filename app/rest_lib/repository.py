from __future__ import annotations
from typing import Callable, NamedTuple, Any
from app.db import db, session


class Repository:
    class PK(NamedTuple):
        ...

    def __init__(self, model: db.Model, filters: dict[str, Callable] = None):
        self._model = model
        self._filters = filters

    @property
    def session(self) -> db.Session:
        return session

    @property
    def model(self) -> db.Model:
        return self._model

    def pk_query(self, pk: PK, model: db.Model = None) -> Any:
        return self.query(model).filter_by(**pk._asdict())

    def query(self, model: db.Model = None) -> db.Query:
        result = self.session.query(model if model else self.model)
        db.Query.custom_filters = lambda query, *params, **kwargs: self.__custom_filters(query, *params, **kwargs)
        db.Query.custom_order_by = lambda query, *params, **kwargs: self.__custom_orders(query, *params, **kwargs)
        return result

    def __custom_filters(self, query: db.Query, filters: list) -> db.Query:
        result = query
        for key in filters:
            result = result.filter(self._filters[key]())
        return result

    @staticmethod
    def __custom_orders(query: db.Query, sort_by: str, reversed: bool) -> db.Query:
        prefix = 'DESC' if reversed else 'ASC'
        return query.order_by(db.text(sort_by + ' ' + prefix))
