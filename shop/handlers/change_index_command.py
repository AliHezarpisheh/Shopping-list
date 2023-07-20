from typing import NoReturn
from shop.utils.basket import Basket
from shop.utils.funcs import (
    show_divider,
    clear_screen,
    guide_message,
)
from shop.helpers.exceptions import (
    ItemDoesNotExistError,
    WrongOrderError
)
from config.log_config import config_logging

logger = config_logging()


def handle_change_index(basket: Basket) -> NoReturn:
    clear_screen()

    items, _ = basket.show()
    print(items)
    print(show_divider())

    item_name = input(
        "Please enter the name of the item you're considering to move: ").title()
    print(show_divider())

    if item_name == "Back":
        clear_screen()
    else:
        str_new_index = input(
            "Enter where you want the item place in your shopping list(enter a number): ")

        if str_new_index.title() == "Back":
            clear_screen()
        else:
            print(show_divider())
            try:
                int_new_index = int(str_new_index)
                try:
                    basket.change_index(item_name, int_new_index)
                except ItemDoesNotExistError as error:
                    print(error)
                except WrongOrderError as error:
                    print(error, "Please try again.")
            except ValueError:
                logger.info("User entered a new index which is not a number.")
                print("You must enter a number. Please try again.")

            print(guide_message())

    print(show_divider())
