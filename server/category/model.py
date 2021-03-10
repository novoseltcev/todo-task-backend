from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from server import Base, config


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(config.category_name_len), unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tasks = relationship('Task', order_by='Task.id')
