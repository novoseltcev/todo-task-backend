from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from server import Base, config


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(config.task_title_len))
    status = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey('categories.id'), )
    files = relationship('File', order_by='File.name')
