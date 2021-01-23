#
# запуск flask-app
#
from server import *
from crud import *

flask_app.template_folder = "static/templates"
flask_app.run(debug=True)
