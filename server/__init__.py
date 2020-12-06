from flask import Flask
from server.server_op import ServerOperationOnDB
from server.data_base import BinDB, IStorage


class App(Flask, ServerOperationOnDB):
    def __init__(self):
        super().__init__(__name__)
        self.init_storage(BinDB())
        self.storage.append_task('test_title')
        print(self.storage.tasks, 'aaaa')


app = App()
