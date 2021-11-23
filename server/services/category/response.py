from __future__ import annotations
from typing import Tuple

from .schema import CategorySchema
from .model import Category


class CategoryResponse(dict):
    @staticmethod
    def dump(category: Category | Tuple[Category], many=False):
        return CategoryResponse(CategorySchema(many=many).dump(category))

    @staticmethod
    def success():
        return CategoryResponse(success=True)
