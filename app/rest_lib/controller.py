from flask import request
from flask.views import MethodView

from app.auth import auth_service
from .services import Service


class Controller(MethodView):
    def __init__(self, service: Service):
        self.service = service
        self._json = None
        self.args = request.args
        self.auth_service = auth_service

    @property
    def json(self):
        if not self._json:
            self._json = request.json
        return self._json

    @property
    def user(self):
        return self.auth_service.user
