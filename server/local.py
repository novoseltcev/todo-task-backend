from flask import Flask, request, send_file, render_template
from os import remove
from server.db.sqlite_db import SQLiteDB

DB = SQLiteDB()

flask_app = Flask(__name__)
flask_app.template_folder = "static/templates"

