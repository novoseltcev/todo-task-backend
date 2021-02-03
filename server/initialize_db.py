from database import Engine
from os import getcwd, path

cwd = getcwd()
engine = Engine(path.join(cwd, 'server', 'data', 'task.db'))
