class Category(object):
    __default = 1

    def __init__(self, name="All"):
        self.name = name

    def change_name(self, new_name):
        self.name = new_name

    def delete(self, tasks, move=False):
        if move:
            self._move_tasks(tasks)
        else:
            self._delete_tasks(tasks)

    def _move_tasks(self, tasks):
        for task in tasks:
            if task.category == self.name:
                task.change_category(self.__default)

    def _delete_tasks(self, tasks):
        for task in tasks:
            if task.category == self.name:
                task.delete()
