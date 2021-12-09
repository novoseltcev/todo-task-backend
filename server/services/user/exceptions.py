class UserException(Exception):
    pass


class UnconfirmedEmailError(UserException):
    pass


class InvalidPasswordError(UserException):
    pass


class InvalidEmailError(UserException):
    pass


class AdminRequiredError(UserException):
    pass


class LoginError(UserException):
    pass


class RegistrationError(UserException):
    pass


class ConfirmationError(UserException):
    pass
