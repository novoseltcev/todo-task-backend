# Класс модели, который описывает сущность предметной области или ее часть
import os

from sqlalchemy import Column, Integer, String, ForeignKey

from server.initialize_db import Base, engine, DB_config


filename_len = DB_config['filename_len']
files_dir_len = DB_config['files_dir_len']


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String(filename_len))
    path = Column(String(files_dir_len + filename_len), unique=True)
    task = Column(Integer, ForeignKey('tasks.id'))

    def __init__(self, name: str, path: str, task: id):
        self.name = name
        self.path = path
        self.task = task

    def change_name(self, new_name: str):
        self.name = new_name

    def _get_full_path(self):
        cwd = os.getcwd()
        return os.path.join(cwd, self.path)

    def save(self, data):
        with open(self._get_full_path(), "wb+") as fp:
            fp.write(data)

    def delete(self):
        os.remove(self._get_full_path())
