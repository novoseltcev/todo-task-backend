from ._serviceABC import CategoryService
from .schema import CategorySchema
from .response import CategoryResponse
from .model import Category

from ._repositoryABC import Categories


class CategoryLogic(CategoryService):
    @classmethod
    def get(cls, schema: CategorySchema) -> CategoryResponse:
        category = Categories.load(schema.id)
        assert category.id_user == schema.id_user  # TODO - add check func
        return CategoryResponse.dump(category)

    @classmethod
    def get_all(cls, schema: CategorySchema) -> CategoryResponse:
        categories = Categories.load_by_user(schema.id_user)
        return CategoryResponse.dump(categories, many=True)

    @classmethod
    def create(cls, schema: CategorySchema) -> CategoryResponse:
        category = Category(id_user=schema.id_user, name=schema.name)
        Categories.save(category)
        return CategoryResponse.success()

    @classmethod
    def edit_name(cls, schema: CategorySchema) -> CategoryResponse:
        category = Categories.load(schema.id)
        assert category.id_user == schema.id_user  # TODO
        category.name = schema.name
        Categories.save(category)
        return CategoryResponse.success()

    @classmethod
    def delete(cls, schema: CategorySchema) -> CategoryResponse:
        category = Categories.load(schema.id)
        assert category.id_user == schema.id_user  # TODO
        Categories.delete(schema.id)
        return CategoryResponse.success()
