import shelve


class DataBase:
    __dictionary = []

    def __init__(self, filename="server\file_db"):
        with shelve.open("file_db") as file:
            self.__dictionary = file.get("db", [])

    def serialization(self, filename="file_db"):
        with shelve.open(filename) as file:
            file["db"] = self.__dictionary

    def append(self, name):
        self.__dictionary.append({
            "id": len(self.__dictionary),
            "name": name,
            "is_done": False
        })

    def remove(self, id):
        for task in self.__dictionary:
            if task["id"] == id:
                self.__dictionary.remove(task)
                return

    def switch_competition(self, id):
        for task in self.__dictionary:
            if task["id"] == id:
                task["is_done"] = not task["is_done"]
                return

    @property
    def dictionary(self):
        return self.__dictionary
