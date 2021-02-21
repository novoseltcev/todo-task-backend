# Класс модели, который описывает сущность предметной области или ее часть
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from server.initialize_db import Base, engine, config


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(config.task_title_len))
    status = Column(Integer, nullable=True)
    category = Column(Integer, ForeignKey('categories.id'))
    files = relationship('File', backref=__tablename__, order_by='File.name')

    def change_title(self, new_title: str):
        self.title = new_title

    def change_status(self):
        self.status = (self.status + 1) % 2

    def change_category(self, new_category):
        self.category = new_category
