from datetime import date

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Date
from werkzeug.security import generate_password_hash, check_password_hash

from server import Base


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(85), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    reg_date = Column(Date)

    def __init__(self, email: str, login: str, password: str):
        self.email = email
        self.login = login
        self.set_password(password)
        self.reg_date = date.today()

    def change_email(self, new_email):
        self.email = new_email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
