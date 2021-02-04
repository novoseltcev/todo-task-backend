# Класс модели, который описывает сущность предметной области или ее часть


class Task(object):

    def __init__(self, title: str, category, status=0):
        self.title = title
        self.category = category
        self.status = status

    def change_title(self, new_title: str):
        self.title = new_title

    def change_status(self):
        self.status = (self.status + 1) % 2

    def change_category(self, new_category):
        self.category = new_category
