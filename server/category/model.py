class Category(object):
    __default = 1

    def __init__(self, name="All"):
        self.name = name

    def change_name(self, new_name):
        self.name = new_name
