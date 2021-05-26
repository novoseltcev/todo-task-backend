from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from server import Base
from server.config import BaseConfig


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(BaseConfig.category_name_len), unique=True, nullable=False)

    tasks = relationship('Task', order_by='Task.id', cascade='all,delete')
