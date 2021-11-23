from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# from server import Base  # TODO
from server.config import BaseConfig


class Category:
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(BaseConfig.category_name_len), unique=True, nullable=False)

    tasks = relationship('Task', order_by='Task.id', cascade='all,delete')


# class newCategory(Base, Category):
#     pass
#
#
# Category = newCategory
