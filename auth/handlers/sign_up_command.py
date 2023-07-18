from getpass import getpass
from pathlib import Path
from auth.utils.funcs import clear_screen, show_divider
from auth.models.user import User
from auth.helpers.exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidUsernameError,
    DuplicateEmailError,
    DuplicateUsernameError,
)
from auth.models.storage import save_existed_users
from config.log_config import config_logging

logger = config_logging()


def handle_sign_up() -> User:
    """
    Handles the user sign-up process and returns the signed-up User object.

    Prompts the user for their desired username, email, and password.
    If the provided information is valid, the user is added to the system and a success message is displayed.
    If any invalid information is entered, an appropriate error message is shown.

    Returns:
        User: The User object representing the signed-up user.
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
            user.check_duplicate()
            user.add_user()

            clear_screen()
            logger.info(f"{user} signed up.")
            print("You have signed up! Enjoy your shopping experience.")

            complete = True
        except (
            TypeError,
            InvalidUsernameError,
            InvalidEmailError,
            InvalidPasswordError,
            DuplicateUsernameError,
            DuplicateEmailError,
        ) as error:
            clear_screen()
            logger.error(error)
            print("Sorry, the provided information is invalid or already exists. Please try again.")
        except Exception as error:
            clear_screen()
            logger.critical(error)
            print("Error 500! Call administrator.")

        print(show_divider())

    # Write in users json file.
    directory = Path.cwd()
    file_path = directory / "auth/models/users.json"

    with file_path.open("w") as users_file:
        User.to_json(structure={"users": User.all_dict}, json_file=users_file)

    return user
