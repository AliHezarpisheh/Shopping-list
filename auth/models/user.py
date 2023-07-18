import bcrypt
from typing import Type, NoReturn
from auth.models.account import Account, ToFile
from auth.helpers.exceptions import (
    InvalidPasswordError,
    GetPassError,
    DuplicateEmailError,
    DuplicateUsernameError,
    SignInError,
)
from config.log_config import config_logging

logger = config_logging()


class User(Account, ToFile):
    """
    Represents a user with a username, email, and password.

    Inherits from:
        Account: Provides the username, email, and password attributes and their associated behavior.
        ToFile: Provides utility methods for writing data to a file.

    Class Attributes:
        all (list): A list of all User instances.
        all_dict (list): A list of dictionaries representing the attributes of all User instances.

    Attributes:
        username (str): The username associated with the user.
        email (str): The email address associated with the user.
        password (str): The password associated with the user.
        is_premium (bool): Indicates whether the user has a premium account.
        is_hashed (bool): Indicates whether the password is already hashed.

    Raises:
        TypeError: If the provided username, email, or password is not a string.
        InvalidUsernameError: If the provided username is not valid (minimum 4 characters starting with A-z, a-z, and can be followed by A-Z, a-z, 0-9, ., -, or _).
        InvalidEmailError: If the provided email address is not valid (does not match the expected email format).
        InvalidPasswordError: If the provided password is not valid (minimum 12 characters required).
        GetPassError: If an attempt is made to get the password attribute.
        DuplicateUsernameError: If the username is already in use by another user.
        DuplicateEmailError: If the email address is already in use by another user.
        SignInError: If the sign-in process fails due to an invalid username or password.
    """

    all = list()
    all_dict = list()

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        is_premium: bool = False,
        is_hashed: bool = False,
    ) -> NoReturn:
        """
        Initializes a new User instance with the provided username, email, password, and account properties.

        Args:
            username (str): The username associated with the user.
            email (str): The email address associated with the user.
            password (str): The password associated with the user.
            is_premium (bool, optional): Indicates whether the user has a premium account. Defaults to False.
            is_hashed (bool, optional): Indicates whether the password is already hashed. Defaults to False.
        """
        self.is_hashed = is_hashed
        self.is_premium = is_premium
        super().__init__(username, email, password)

    @property
    def password(self) -> NoReturn | GetPassError:
        """
        Get the password associated with the user. Raises a GetPassError.

        Returns:
            NoReturn | GetPassError: No return value; raises a GetPassError.
        """
        logger.warning("Someone tried to get the password.")
        raise GetPassError("Password is just writable.")

    @password.setter
    def password(self, value: str) -> NoReturn | InvalidPasswordError:
        """
        Set the password associated with the user.

        Args:
            value (str): The new password value.

        Raises:
            TypeError: If the provided password is not a string.
            InvalidPasswordError: If the provided password is not valid (minimum 12 characters required).

        Notes:
            - If `is_hashed` is set to `True`, the provided password is assumed to be already hashed and is stored as-is.
            - If `is_hashed` is set to `False` (default), the provided password is hashed using bcrypt before storing it.
        """
        if not isinstance(value, str):
            raise TypeError(f"String expected, got {type(value)}")
        elif len(value) < 12:
            raise InvalidPasswordError(
                "Please provide a valid password format(minimum 12 characters)"
            )
        else:
            if self.is_hashed:
                self._hashed_password = value
            else:
                salt = b"$2b$12$UJ9EnzPabmOZYRlcphuqdO"
                hashed_password = bcrypt.hashpw(value.encode("utf-8"), salt)
                self._hashed_password = hashed_password.decode()

        del self.is_hashed

    def check_duplicate(
        self,
    ) -> NoReturn | DuplicateUsernameError | DuplicateEmailError:
        """
        Check for duplicate usernames or email addresses among all users.

        Raises:
            DuplicateUsernameError: If the username is already in use by another user.
            DuplicateEmailError: If the email address is already in use by another user.
        """
        for user in self.__class__.all:
            if self.username == user.username:
                raise DuplicateUsernameError(
                    "Username is already in use! Try another one."
                )

        for user in self.__class__.all:
            if self.email == user.email:
                raise DuplicateEmailError("Email is already in use! Try another one.")

    def sign_in(self) -> Type["User"] | SignInError:
        """
        Attempt to sign in the user.

        Returns:
            Type['User'] | SignInError: The signed-in User object if the sign-in is successful, or a SignInError if unsuccessful.

        Raises:
            SignInError: If the sign-in process fails due to an invalid username or password.
        """
        for user in self.__class__.all:
            if user.__dict__ == self.__dict__:
                return user
        logger.info(f"User {self.__dict__} haven't signed up but wants to sign in.")
        raise SignInError(f"Invalid username or password. {self} haven't signed up.")

    def add_user(self) -> NoReturn:
        """add the user to the list of all users."""
        User.all.append(self)
        User.all_dict.append(self.__dict__)

    def __repr__(self) -> str:
        """Get the string representation of the User instance."""
        return f"{self.__class__.__name__}{self._username, self._email}"
