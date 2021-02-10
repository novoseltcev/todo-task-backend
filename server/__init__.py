from server.app import app
from server import errors_handler
from server.category import controller
# from server.task import controller
from server.file import controller
import server.index

__all__ = ['controller', 'index', 'app']
__version__ = "0.1"
