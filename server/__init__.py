#
# инициализация и сборка пакета для run.py
#
from server.init_app import flask_app
from server.init_db import DB
__version__ = "0.3"
__all__ = ['flask_app', 'DB']

