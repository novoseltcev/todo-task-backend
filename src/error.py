class NotFoundError(Exception):
    """Raises when object wasn't found."""


class DataUniqueError(Exception):
    """Raises when trying to set data that should be unique."""


class LoginError(Exception):
    """Raises when the authorization error occurred."""


class RegistrationError(Exception):
    """Raises when the registration error occurred."""
