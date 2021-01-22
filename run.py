#
# запуск flask-app
#
from server import *
from server.crud import *
from server.handler import *


flask_app.run(debug=True)
