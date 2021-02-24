from database.manager import DBManager

from .model import User


class UserRepository(DBManager):
    def __init__(self):
        super().__init__(User)

    def get_by_primary(self, id: int):
        return self._get_by(all_rows=False, id=id)

    @DBManager.session_handler
    def insert(self, login: str, email: str, password: str):
        self._insert(login=login, email=email, password=password)

    @DBManager.session_handler
    def update_email(self, id: int, email: str):
        task = self._get_by(id=id)
        task.change_email(email)

    @DBManager.session_handler
    def update_password(self, id: int, password: str):
        task = self._get_by(id=id)
        task.change_password(password)

    @DBManager.session_handler
    def delete(self, id: int):
        self._delete(id)
