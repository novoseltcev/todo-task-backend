# Класс модели, который описывает сущность предметной области или ее часть
import os


class File(object):
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def change_name(self, new_name: str):
        self.name = new_name

    def get_full_path(self):
        cwd = os.getcwd()
        return os.path.join(cwd, 'data', self.path)

    def save(self, data):
        with open(self.get_full_path(), "wb+") as fp:
            fp.write(data)

    def delete(self):
        os.remove(self.get_full_path())
