from typing import NoReturn
from shop.models.products import Product
from shop.utils.basket import Basket
from shop.utils.funcs import (
    show_help,
    show_divider,
    clear_screen,
)
from shop import COMMANDS
from auth.utils.consts import USER_INTENT
from config.log_config import config_logging

logger = config_logging()


def main() -> NoReturn:
    """Execute the main logic of the shopping store application."""
    clear_screen()
    logger.debug("App has been started.")
    print("Welcome to TechWorld, your one-stop shop for all your tech device needs!")
    print(show_divider())

    # authentication
    while True:
        user_intent = input("Sign up/Sign in: ").lower()
        clear_screen()

        if user_intent in USER_INTENT:
            authentication_action = USER_INTENT[user_intent]
            user = authentication_action()
            break

    # Shop
    basket = Basket()
    print(show_help())

    while True:
        action = input(f"({user.username}) Which action are you considering: ")
        action = action.lower()

        if action in COMMANDS:
            exec_action = COMMANDS[action]
            exec_action(basket)

        elif action == "products":
            clear_screen()
            Product.show_all()
            print(show_divider())

        elif action == "show":
            clear_screen()
            items, final_price = basket.show()
            print(items)
            print("\nHere is your final price after tax: {:.2f}$".format(final_price))
            print(show_divider())

        elif action == "help":
            clear_screen()
            print(show_help())

        elif action == "quit":
            clear_screen()
            items, final_price = basket.show()
            print(items)
            print("\nHere is your final price after tax: {:.2f}$".format(final_price))
            break

        else:
            print(show_divider())
            print("Wrong action, enter help for reviewing action's guideline")
            print(show_divider())
