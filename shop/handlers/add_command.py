from shop.utils.funcs import (
    add_items,
    title_and_strip_items,
    show_divider,
    clear_screen,
    guide_message,
    show_products
)
from shop.helpers.exceptions import ItemDoesNotExist
from shop.models import get_all_products
from shop.helpers.type_hints import (
    Basket,
    Products,
    ProductNames
)
from config.log_config import config_logging

logger = config_logging()


def handle_add_command(basket: Basket) -> Basket:
    """Handle the 'add' command by allowing the user to select and add products to the shopping basket.

    Args:
        basket (Basket): The current shopping basket.

    Returns:
        Basket: The updated shopping basket after adding the selected products.
    """
    clear_screen()

    all_products: Products = get_all_products()
    show_products(all_products)
    print(show_divider())

    additional_items = input(
        "Enter the name(s) which represents the product(s) you're considering to add: ").split(",")

    try:
        additional_items: ProductNames = title_and_strip_items(additional_items)
    except TypeError:
        logger.error("Data type of the arguments were not correct. check title_and_strip_items function.")
        print("Please try again entering the items. Be sure that you're entering valid items. Call the administrator if the issue is not solved.")

    if additional_items[0] == "Back":
        clear_screen()
    else:
        clear_screen()
        try:
            basket = add_items(all_products, basket, additional_items)
        except ItemDoesNotExist as error:
            print(error, "Type and Enter products for seeing products.")
        except Exception as error:
            logger.critical(error)
            print("Error 500! Call the Administrator.")
        print(guide_message())

    print(show_divider())

    return basket
