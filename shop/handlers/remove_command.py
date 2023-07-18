from shop.utils.funcs import (
    remove_items,
    title_and_strip_items,
    show_divider,
    clear_screen,
    guide_message,
    show_basket
)
from shop.helpers.exceptions import ItemDoesNotExist
from shop.helpers.type_hints import (
    Basket,
    ProductNames
)
from config.log_config import config_logging

logger = config_logging()


def handle_remove_command(basket: Basket) -> Basket:
    """Handle the 'remove' command by allowing the user to select and remove products from the shopping basket.

    Args:
        basket (Basket): The current shopping basket.

    Returns:
        Basket: The updated shopping basket after removing the selected products.
    """
    clear_screen()
    items, _ = show_basket(basket)
    print(items)
    print(show_divider())

    items_to_delete = input(
        "Enter the name(s) which represents the product(s) you're considering to remove: ").split(",")

    try:
        items_to_delete: ProductNames = title_and_strip_items(items_to_delete)
    except TypeError:
        logger.error("Data type of the arguments were not correct. check title_and_strip_items function.")
        print("Please try again entering the items. Be sure that you're entering valid items. Call the administrator if the issue is not solved.")

    if items_to_delete[0] == "Back":
        clear_screen()
    else:
        clear_screen()
        try:
            basket = remove_items(basket, items_to_delete)
        except ItemDoesNotExist as error:
            print(error, "Type and Enter show for seeing your basket.")
        except Exception as error:
            logger.critical(error)
            print("Error 500! Call the Administrator.")
        print(guide_message())

    print(show_divider())

    return basket
