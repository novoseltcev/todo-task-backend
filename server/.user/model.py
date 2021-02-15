from datetime import date

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Date

from server.initialize_db import Base, engine


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(25), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    reg_date = Column('reg_date', Date)

    def __init__(self, email: str, login: str, password: str):
        self.email = email
        self.login = login
        self.password = password
        self.reg_date = date.today()

    def change_email(self, new_email):
        self.email = new_email


Base.metadata.create_all(bind=engine)