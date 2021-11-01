class APIRouter:  # TODO
    @staticmethod
    def init_app(wsgi_app):
        from server.api.mail import email_blueprint
        from server.errors import error_blueprint
        from server.views import view_blueprint
        from server.api.user import user_blueprint
        from server.api.category import category_blueprint
        from server.api.task import task_blueprint
        from server.api.file import file_blueprint
        wsgi_app.register_blueprint(email_blueprint)
        wsgi_app.register_blueprint(error_blueprint)
        wsgi_app.register_blueprint(view_blueprint)
        wsgi_app.register_blueprint(task_blueprint)
        wsgi_app.register_blueprint(category_blueprint)
        wsgi_app.register_blueprint(file_blueprint)
        wsgi_app.register_blueprint(user_blueprint)
