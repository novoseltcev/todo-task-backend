class CustomException(Exception):
    def __init__(self, http_code, message, **params):
        self.http_code = http_code
        self.message = message
        self.body = {**params}

    @property
    def json(self):
        return {
            'error': type(self).__name__,
            'msg': self.message,
            'body': self.body
        }


class Unauthorized(CustomException):
    def __init__(self, message: str = 'Пользователь не авторизован.'):
        super(type(self), self).__init__(http_code=401, message=message)


class Forbidden(CustomException):
    def __init__(self, message: str = 'Пользователю запрещена данная операция.'):
        super(type(self), self).__init__(http_code=403, message=message)


class NoSuchEntityError(CustomException):
    def __init__(self, message: str = 'Нет такой сущности.'):
        super(type(self), self).__init__(http_code=404, message=message)


class LogicError(CustomException):
    def __init__(self, message='Логическая ошибка.'):
        super(LogicError, self).__init__(http_code=409, message=message)


class ChangeCategoryError(LogicError):
    def __init__(self):
        super(ChangeCategoryError, self).__init__(message='Нет прав на изменение категории')