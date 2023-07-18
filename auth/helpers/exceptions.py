class InvalidEmailError(ValueError):
    """Raised when an invalid email address is provided."""
    pass


class InvalidPasswordError(ValueError):
    """Raised when an invalid password is provided."""
    pass


class InvalidUsernameError(ValueError):
    """Raised when an invalid username is provided."""
    pass


class GetPassError(AttributeError):
    """Raised when an error occurs while using getpass to retrieve user input."""
    pass


class DuplicateUsernameError(Exception):
    """Raised when a duplicate username is detected during sign-up."""
    pass


class DuplicateEmailError(Exception):
    """Raised when a duplicate email is detected during sign-up."""
    pass


class SignInError(Exception):
    """Raised when an error occurs during the sign-in process."""
    pass