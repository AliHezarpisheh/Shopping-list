import json
from pathlib import Path
from typing import NoReturn
from auth.models.user import User
from config.log_config import config_logging

logger = config_logging()

directory = Path.cwd()
file_path = directory / "auth/models/users.json"

try:
    with file_path.open(mode="r") as users_file:
        data = json.load(users_file)
        users = data.get("users", [])
except:
    logger.critical("Something went wrong in users file opening.")
    users = list()


def save_existed_users() -> NoReturn:
    """Saves existing users from a JSON file to the system."""
    for user in users:
        username, email, password, is_premium = (
            user["_username"],
            user["_email"],
            user["_hashed_password"],
            user["is_premium"],
        )
        user = User(username, email, password, is_premium, is_hashed=True)
        user.add_user()
