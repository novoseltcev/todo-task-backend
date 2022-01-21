from random import choice
from copy import deepcopy, copy
from typing import List, Callable

from mock import Mock
import pytest

from server.category.business.service import (
    CategoryRepository, Category,
    CategoryService, CategoryInputData,
)
from server.error import NotFoundError


def category_id_pred(category: Category):
    return category.identity


def account_pred(category: Category):
    return category.account


list_accounts = [0, 1]
list_categories = [Category.Generator.example(i, list_accounts[0]) for i in range(2)]

invalid_categories_id = [
    (-1, choice(list_categories).account),
    (1 + max(list_categories, key=category_id_pred).identity, choice(list_categories).account),
]
invalid_accounts = [
    (choice(list_categories).identity, -1),
    (choice(list_categories).identity, max(list_categories, key=account_pred).account + 1),
]

invalid_sets = invalid_categories_id + invalid_accounts


def categories_by_tuple(account: int):
    return tuple(filter(lambda category: category.account == account, list_categories))


class FakeCategories(CategoryRepository, Mock):
    """Mocking repository class to service"""

    def __init__(self):
        super().__init__()
        self.categories = deepcopy(list_categories)

    def from_id(self, identity: int) -> Category:
        return copy(self.contain(lambda category: category.identity == identity)[0])

    def from_account(self, account_id: int) -> List[Category,]:
        return deepcopy(self._custom_filter(lambda category: category.account == account_id))

    def insert(self, category: Category) -> int:
        newest_id = 1 + max(self.categories, key=lambda _category: _category.identity, default=-1).identity
        self.categories.append(
            Category(category.name, category.account, newest_id))
        return newest_id

    def save(self, category: Category) -> None:
        category_in_system = self.contain(
            lambda _category: _category.identity == category.identity)[0]
        category_in_system.name = category.name

    def remove(self, category: Category) -> None:
        category_in_system = self.contain(
            lambda _category: _category.identity == category.identity)[0]
        self.categories.remove(category_in_system)

    def contain(self, pred: Callable):
        result = self._custom_filter(pred)
        if len(result) == 0:
            raise NotFoundError()
        return result

    def _custom_filter(self, pred: Callable):
        return list(filter(pred, self.categories))


@pytest.fixture
def random_category():
    return choice(list_categories)


@pytest.fixture
def last_id():
    return max(list_categories, key=lambda category: category.identity).identity


class TestCategoryService:
    """UnitTests to CategoryService"""

    def setup_method(self, method):
        self.service = CategoryService(FakeCategories)

    @pytest.mark.parametrize(
        'identity, account_id, category',
        [(category.identity, category.account, category) for category in list_categories])
    def test_get__found(self, identity: int, account_id: int, category: Category):
        assert self.service.get(identity, account_id) == category

    @pytest.mark.parametrize('identity, account_id', invalid_sets)
    def test_get__not_found_error(self, identity: int, account_id: int):
        with pytest.raises(NotFoundError):
            self.service.get(identity, account_id)

    @pytest.mark.parametrize(
        'account_id, categories_tuple',
        [(account, categories_by_tuple(account))
            for account in set(map(lambda category: category.account, list_categories))])
    def test_get_all__found(self, account_id, categories_tuple):
        assert self.service.get_all(account_id) == categories_tuple

    def test_create__done(self, random_category, last_id):
        account_id: int = random_category.account
        data: CategoryInputData = CategoryInputData("example")
        assert self.service.create(account_id, data) == last_id + 1
        category = self.service.get(last_id + 1, account_id)
        assert category.name == data.name

    @pytest.mark.parametrize(
        'identity, account_id, name',
        [(category.identity, category.account, category.name) for category in list_categories] +
        [(category.identity, category.account, 'new_category-{i}')
            for i, category in enumerate(list_categories)])
    def test_update__done(self, identity: int, account_id: int, name: str):
        data = CategoryInputData(name)
        self.service.update(identity, account_id, data)
        category = self.service.get(identity, account_id)
        assert category.name == data.name

    @pytest.mark.parametrize('identity, account_id', invalid_sets)
    def test_update__not_found_error(self, identity: int, account_id: int):
        with pytest.raises(NotFoundError):
            self.service.update(identity, account_id, CategoryInputData('example'))

    @pytest.mark.parametrize(
        'identity, account_id',
        [(category.identity, category.account) for category in list_categories])
    def test_delete__done(self, identity: int, account_id: int):
        self.service.delete(identity, account_id)
        with pytest.raises(NotFoundError):
            self.service.get(identity, account_id)

    @pytest.mark.parametrize('identity, account_id', invalid_sets)
    def test_delete__not_found_error(self, identity, account_id: int):
        with pytest.raises(NotFoundError):
            self.service.delete(identity, account_id)
