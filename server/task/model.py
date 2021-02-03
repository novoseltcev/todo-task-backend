# Класс модели, который описывает сущность предметной области или ее часть
from server.category.model import Category
from server.file.model import File


class Task(object):
    files = []

    def __init__(self, title: str, category=Category('All'), status=0):
        self.title = title
        self.category = category
        self.status = status

    def change_title(self, new_title: str):
        self.title = new_title

    def change_status(self):
        self.status = (self.status + 1) % 2

    def change_category(self, new_category: Category):
        self.category = new_category

    def append_file(self, file: File):
        self.files.append(file)

    def remove_file(self, file: File):
        self.files.remove(file)
        file.delete()

    def delete(self):
        for file in self.files:
            file.delete()
