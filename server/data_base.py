import shelve
from flask import abort
from server.istorage import IStorage


class BinDB(IStorage):

    def __init__(self, filename="server\\data"):
        super().__init__()
        with shelve.open(filename + '\\file_db') as file:
            self.__counter = file.get('max_id', 0)
            self.tasks = file.get("db", [])
            self.categories = file.get("categories", [])

    def __serialization(self, filename="server\\data"):
        with shelve.open(filename + '\\file_db') as file:
            file['max_id'] = self.__counter
            file["db"] = self.tasks
            file["categories"] = self.categories

    def append_task(self, title_task: str):
        self.__counter += 1
        self.tasks.append({
            "id": self.__counter,
            "title": title_task,
            'category': self.current_category,
            "is_done": False
        })
        self.__serialization()

    def append_category(self, category: str):
        if self.categories.count(category) == 0:
            self.categories.append(category)

        self.current_category = category
        self.__serialization()

    def update_task_status(self, task_id: int):
        searched_task = self.search_by_id(task_id)
        if searched_task is not None:
            searched_task['is_done'] = not searched_task['is_done']
            self.__serialization()

    def update_task_category(self, task_id: int, category: str):
        searched_task = self.search_by_id(task_id)
        if searched_task is not None:
            searched_task['category'] = category
            self.__serialization()

    def rename_category(self, destination: str, source: str):
        for el in self.tasks:
            if el['category'] == destination:
                el['category'] = source

        self.categories.remove(destination)
        self.categories.append(source)
        self.__default_category(destination)
        self.__serialization()

    def remove_task(self, task_id: int):
        searched_task = self.search_by_id(task_id)
        if searched_task is not None:
            self.tasks.remove(searched_task)
            self.__serialization()

    def remove_category(self, category: str):  #  TODO - S from SOLID
        if category == self.__default:
            abort(500)
        for el in self.tasks:
            if el["category"] == category:
                self.tasks.remove(el)
        self.categories.remove(category)
        self.current_category = self.__default
        self.__serialization()

    def search_by_id(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        abort('404')
        return None

    def filter(self):
        if self.current_category != self.__default:
            result = []
            for el in self.tasks:
                if el['category'] == self.current_category:
                    result.append(el)
            self.tasks = result

    def copy(self):
        result = BinDB("server\\data\\temp")
        result.tasks = self.tasks.copy()
        result.categories = self.categories.copy()
        result.current_category = self.current_category
        return result

    def __default_category(self, source):
        if self.current_category == source:
            self.current_category = self.__default

