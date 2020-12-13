from flask import Flask
from server.server_op import ServerOperationOnDB
from server.data_base import BinDB, IStorage
from server.sqlite_db import SQLiteDB


class App(Flask, ServerOperationOnDB):
    def __init__(self):
        super().__init__(__name__)
        self.init_storage(SQLiteDB())


app = App()
