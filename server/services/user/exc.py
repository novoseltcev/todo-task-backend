class UserException(Exception):
    pass


class NotFoundError(UserException):
    pass


class UnconfirmedEmailError(UserException):
    pass


class EmailError(UserException):
    pass


class PasswordError(UserException):
    pass


class AdminRequiredError(UserException):
    pass


class LoginError(UserException):
    pass
