class NotFoundError(Exception):
    """Raises when object wasn't found."""
    pass


class DataUniqueError(Exception):
    """Raises when trying to set data that should be unique."""
    pass


class LoginError(Exception):
    """Raises when the authorization error occurred."""
    pass


class RegistrationError(Exception):
    """Raises when the registration error occurred."""
    pass
