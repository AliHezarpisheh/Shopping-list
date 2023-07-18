from getpass import getpass
from auth.models.user import User
from auth.utils.funcs import clear_screen, show_divider
from auth.helpers.exceptions import (
    InvalidUsernameError,
    InvalidEmailError,
    InvalidPasswordError,
    SignInError,
)
from auth.models.storage import save_existed_users
from config.log_config import config_logging

logger = config_logging()


def handle_sign_in() -> User:
    """
    Handles the user sign-in process and returns the signed-in User object.

    Prompts the user for their username, email, and password.
    If the provided information is valid, the user is signed in and a success message is displayed.
    If any invalid information is entered, an appropriate error message is shown.

    Returns:
        User: The User object representing the signed-in user.
    """
    clear_screen()
    save_existed_users()

    complete: bool = False
    while not complete:
        username = input("Username: ")
        print(show_divider())

        email = input("Email: ")
        print(show_divider())

        password = getpass("Password: ")
        print(show_divider())

        try:
            user = User(username, email, password)
            user = user.sign_in()

            clear_screen()
            print("Great! You are signed in. Enjoy your shopping experience.")
            complete = True
        except (
            TypeError,
            InvalidEmailError,
            InvalidPasswordError,
            InvalidUsernameError,
            SignInError,
        ) as error:
            clear_screen()
            logger.info(error)
            print("We're sorry, but the account information you provided is invalid. Please double-check your credentials and try again.")
        except Exception as error:
            clear_screen()
            logger.critical(error)
            print(error)

        print(show_divider())

    return user
