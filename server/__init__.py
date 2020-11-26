from flask import Flask
from server.data_base import DataBase

app = Flask(__name__)
db = DataBase()


from server import views, crud

