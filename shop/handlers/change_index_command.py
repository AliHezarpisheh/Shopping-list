from shop.utils.funcs import (
    change_index,
    show_divider,
    clear_screen,
    guide_message,
    show_basket
)
from shop.helpers.exceptions import (
    ItemDoesNotExist,
    WrongOrderError
)
from shop.helpers.type_hints import Basket
from config.log_config import config_logging

logger = config_logging()


def handle_change_index(basket: Basket) -> Basket:
    """Handle the change index command by allowing the user to move an item within the shopping basket.

    Args:
        basket (Basket): The current shopping basket.

    Returns:
        Basket: The updated shopping basket after moving the item.
    """
    clear_screen()
    items, _ = show_basket(basket)
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
                    basket = change_index(basket, item_name, int_new_index)
                except ItemDoesNotExist as error:
                    print(error)
                except WrongOrderError as error:
                    print(error, "Please try again.")
            except ValueError:
                logger.info("User entered a new index which is not a number.")
                print("You must enter a number. Please try again.")

            print(guide_message())

    print(show_divider())

    return basket
