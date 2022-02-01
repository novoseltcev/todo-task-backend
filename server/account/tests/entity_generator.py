from datetime import date

from .. import Account


class Generator:
    """Class to generate users examples for tests."""

    @staticmethod
    def get(identity: int, name: str, role: Account.Role, status: Account.Status) -> Account:
        return Account(
            name,
            f'{name}@domen.com',
            Account.generate_password(name),
            role,
            status,
            date(2012, 12, 12),
            identity
        )

    @classmethod
    def user(cls, identity: int, status: Account.Status) -> Account:
        return cls.get(identity, f'User<{identity}>', Account.Role.USER, status)

    @classmethod
    def admin(cls, identity: int, status: Account.Status) -> Account:
        return cls.get(identity, f'Admin<{identity}>', Account.Role.ADMIN, status)

    @classmethod
    def owner(cls, identity: int, status: Account.Status) -> Account:
        return cls.get(identity, f'Owner<{identity}>', Account.Role.OWNER, status)

    @classmethod
    def example(cls, identity: int) -> Account:
        return cls.user(identity, Account.Status.CONFIRMED)
