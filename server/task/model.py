from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from server import Base
from server.config import BaseConfig


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_category = Column(Integer, ForeignKey('categories.id'), nullable=False)
    title = Column(String(BaseConfig.task_title_len), nullable=False)
    status = Column(Boolean, default=False)

    files = relationship('File', order_by='File.name')
