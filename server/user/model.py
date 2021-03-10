from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from server import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(85), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    reg_date = Column(Date)
    categories = relationship('Category', order_by='Category.id')
