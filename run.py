#
# запуск flask-app
#
import server


# with open('this.pdf', 'rb') as f:
#     s = f.read()
#     print(s)
#
# with open('output.bin', 'wb+') as f:
#     f.write(s)


server.flask_app.run(debug=True)
