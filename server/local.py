from server.db.sqlite_db import SQLiteDB
from flask import Flask


DB = SQLiteDB()

flask_app = Flask(__name__)
flask_app.template_folder = "static/templates"
