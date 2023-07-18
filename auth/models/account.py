import json
import re
from typing import Dict, TextIO, NoReturn
from auth.helpers.exceptions import (
    InvalidEmailError,
    InvalidUsernameError,
)
from config.log_config import config_logging

logger = config_logging()


class Account:
    """
    Represents a account with a username, email, and password.

    Attributes:
        username (str): The username associated with the account.
        email (str): The email address associated with the account.
        password (str): The password associated with the account.

    Raises:
        TypeError: If the provided username or email is not a string.
        InvalidUsernameError: If the provided username is not valid (does not match the expected username format).
        InvalidEmailError: If the provided email address is not valid (does not match the expected email format).
    """

    def __init__(self, username: str, email: str, password: str) -> NoReturn:
        """
        Initializes a new Account instance with the provided username, email, and password.

        Args:
            username (str): The username associated with the account.
            email (str): The email address associated with the account.
            password (str): The password associated with the account.
        """
        self.username = username
        self.email = email
        self.password = password

    @property
    def username(self) -> str:
        """
        Get the username associated with the account.

        Returns:
            str: The username associated with the account.
        """
        return self._username

    @username.setter
    def username(self, value: str) -> NoReturn | TypeError | InvalidUsernameError:
        """
        Set the username associated with the account.

        Args:
            value (str): The new username value.

        Raises:
            TypeError: If the provided username is not a string.
            InvalidUsernameError: If the provided username is not valid.
        """
        pattern = r"^(?=.{4,20}$)[a-zA-Z][a-zA-z0-9\._-]+$"
        regex = re.search(pattern, value)

        if not isinstance(value, str):
            raise TypeError(f"String expected, got {type(value)}")
        elif not regex:
            raise InvalidUsernameError(
                "Please provide a valid username(Minimum 4 characters starts with A-z, a-z and can continued by: A-Z, a-z, 0-9, ., - and _)."
            )
        else:
            self._username = value.lower()

    @property
    def email(self) -> str:
        """
        Get the email address associated with the account.

        Returns:
            str: The email address associated with the account.
        """
        return self._email

    @email.setter
    def email(self, value: str) -> NoReturn | TypeError | InvalidEmailError:
        """
        Set the email address associated with the account.

        Args:
            value (str): The new email address value.

        Raises:
            TypeError: If the provided email address is not a string.
            InvalidEmailError: If the provided email address is not valid.
        """
        pattern = r"^(?=.{5,254}$)([a-zA-Z0-9._-]+)@{1}([\w]+)\.([a-zA-Z]{1,3})$"
        regex = re.search(pattern, value)

        if not isinstance(value, str):
            raise TypeError(f"String expected, got {type(value)}")
        elif not regex:
            raise InvalidEmailError("Please provide a valid email format.")
        else:
            self._email = value.lower()


class ToFile:
    """Provides utility methods for writing data to a file."""
    @staticmethod
    def to_json(structure: Dict[str, dict], json_file: TextIO) -> NoReturn:
        """
        Write the given dictionary structure to a JSON file.

        Args:
            structure (Dict[str, dict]): The dictionary structure to be written.
            json_file (TextIO): The file object to write the JSON data.
        """
        json.dump(structure, json_file, indent=4, sort_keys=True)
