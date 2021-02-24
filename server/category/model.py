from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from server import Base, config


class Category(Base):
    __default = 1
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(config.category_name_len), unique=True)
    tasks = relationship('Task', backref=__tablename__, order_by='Task.id')
