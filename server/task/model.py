# Класс модели, который описывает сущность предметной области или ее часть
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from server import Base, engine, config


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(config.task_title_len))
    status = Column(Integer, nullable=True)
    category = Column(Integer, ForeignKey('categories.id'))
    files = relationship('File', backref=__tablename__, order_by='File.name')
