# Класс модели, который описывает сущность предметной области или ее часть
import os

from sqlalchemy import Column, Integer, String, ForeignKey

from server import Base, config


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String(config.filename_len))
    path = Column(String(config.files_dir_len + config.filename_len), unique=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
