# Класс модели, который описывает сущность предметной области или ее часть
import os


class File(object):
    def __init__(self, name: str, path: str):
        self.file_name = name
        self.file_path = path

    def change_name(self, new_name: str):
        self.file_name = new_name

    def _get_full_path(self):
        cwd = os.getcwd()
        return os.path.join(cwd, 'data', self.file_path)

    def save(self, data):
        with open(self._get_full_path(), "wb+") as fp:
            fp.write(data)

    def delete(self):
        os.remove(self._get_full_path())
