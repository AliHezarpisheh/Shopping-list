import os
from typing import NoReturn
from shop.utils.decorators import apply_tax
from config.log_config import config_logging
from shop.helpers.exceptions import (
    ItemDoesNotExist,
    WrongOrderError
)
from shop.helpers.type_hints import (
    Basket,
    Products,
    ProductNames
)

logger = config_logging()


def get_item_by_name(all_products: Products, item_names: ProductNames) -> Products | ItemDoesNotExist:
    """Retrieve a list of products by their names from the given products list.

    Args:
        all_products (Products): The list of all available products.
        item_names (ProductNames): The names of the items to retrieve.

    Returns:
        Products | ItemDoesNotExist: The list of products matching the given names, or raises ItemDoesNotExist
            if any of the names are not found in the products list.

    Raises:
        ItemDoesNotExist: If any of the item names are not found in the products list.

    Example:
        products = get_all_products()
        item_names = ["Apple", "Banana", "Orange"]
        matching_items = get_item_by_name(products, item_names)
        # matching_items contains the products with names "Apple", "Banana", and "Orange"
    """
    for item in item_names:
        for product in all_products:
            if item == product.name:
                break
        else:
            logger.info(f"{item} was not defined in the products list.")
            raise ItemDoesNotExist(f"{item} does not exist in the products(Pay attention to the spelling of words).")

    return list(filter(lambda item: item.name in item_names, all_products))


def add_items(all_products: Products, basket: Basket, new_items: ProductNames) -> Basket:
    """Add new items to the shopping basket, increasing the unit count if the item already exists.

    Args:
        all_products (Products): The list of all available products.
        basket (Basket): The current shopping basket.
        new_items (ProductNames): The names of the new items to add.

    Returns:
        Basket: The updated shopping basket after adding the new items.

    Example:
        products = get_all_products()
        basket = []
        new_items = ["Apple", "Banana", "Orange"]
        updated_basket = add_items(products, basket, new_items)
        # updated_basket contains the shopping basket with the new items added
    """
    new_basket = basket
    new_products = get_item_by_name(all_products, new_items)

    for product in new_products:
        product = product._asdict()
        is_found = False

        for item in new_basket:
            if product["name"] == item["name"]:
                is_found = True
                item["unit"] += 1

                logger.debug(f"{item['name']} unit has been increased by 1 in user's basket.")
                print(f"{item['name']} unit has been increased by 1.")

        if not is_found:
            product["unit"] = 1
            new_basket.append(product)
            logger.debug(f"{product['name']} has been added to user's basket.")
            print(f"{product['name']} has been added to your basket!")

    return new_basket


def remove_items(basket: Basket, removal_items: ProductNames) -> Products:
    """Remove specified items from the shopping basket, decreasing the unit count if the item exists.

    Args:
        basket (Basket): The current shopping basket.
        removal_items (ProductNames): The names of the items to remove.

    Returns:
        Products: The updated shopping basket after removing the items.

    Example:
        basket = get_current_basket()
        removal_items = ["Apple", "Banana"]
        updated_basket = remove_items(basket, removal_items)
        # updated_basket contains the shopping basket with the specified items removed
    """
    new_basket = basket
    removal_items = [name for name in removal_items if any(name == item_name.get("name") for item_name in basket)]
    for item in new_basket:
        if item["name"] in removal_items:
            if item["unit"] > 1:
                item["unit"] -= 1
                removal_items.remove(item["name"])
                print(f"{item['name']} unit has been decreased by 1.")

    new_basket = list(filter(lambda item: item["name"] not in removal_items, new_basket))

    for item in removal_items:
        print(f"{item} has been deleted from your basket!")

    return new_basket


def search_item(basket: Basket, item_name: int) -> str:
    """Search for an item in the shopping basket and return a message indicating its presence."""
    message = "Your considered item is not in your basket."
    for item in basket:
        if item["name"] == item_name:
            message = "Your considered item is in your basket."
    logger.debug("User searched basket successfully.")

    return message


def change_index(basket: Basket, item_name: str, new_index: int) -> Basket | ItemDoesNotExist | WrongOrderError:
    """Change the index of an item in the shopping basket.

    Args:
        basket (Basket): The current shopping basket.
        item_name (str): The name of the item to change the index.
        new_index (int): The new index to move the item to.

    Returns:
        Basket | ItemDoesNotExist | WrongOrderError: The updated shopping basket after changing the item's index,
            or raises ItemDoesNotExist if the item is not found in the basket,
            or raises WrongOrderError if the new index is invalid.

    Raises:
        ItemDoesNotExist: If the item is not found in the basket.
        WrongOrderError: If the new index is invalid (out of range).

    Example:
        basket = get_current_basket()
        item_name = "Apple"
        new_index = 3
        updated_basket = change_index(basket, item_name, new_index)
        # updated_basket contains the shopping basket with the item moved to the new index
    """
    if (new_index >= len(basket)) or (new_index <= 0):
        logger.info(f"The considered order({new_index}) does not exist in user's basket.")
        raise WrongOrderError(f"The considered order({new_index}) does not exist in basket.")
    new_basket = basket
    for item in new_basket:
        if item["name"] == item_name:
            new_basket.remove(item)
            new_basket.insert(new_index - 1, item)
            print(f"{item['name']} has been moved to the {new_index}rd place!")
            logger.debug(f"{item['name']} has been moved to the {new_index}rd place in user's basket.")
            break
    else:
        logger.info(f"{item_name} was not in customer's basket while changing index")
        raise ItemDoesNotExist(f"{item_name} does not exist in your basket(Pay attention to the spelling of words).")

    return new_basket


def count_items(basket: Basket) -> str:
    """Returns a message stating the number of distinct products in the shopping list and provides further instructions."""
    if len(basket) == 0:
        message = "You have no items in your basket."
    message = f"You have {len(basket)} distinct product in your basket."
    message += "\nTo view more details of your basket, please enter: show"
    logger.debug("Counted successfully.")

    return message


def show_products(all_products: Products) -> NoReturn:
    """Display the available products in a paginated manner.

    Args:
        all_products (Products): The list of all available products.

    Returns:
        NoReturn

    Example:
        products = get_all_products()
        show_products(products)
    """
    products_count = len(all_products)
    total_pages = products_count // 5 if products_count % 5 == 0 else (products_count // 5) + 1

    page = 1
    while True:
        clear_screen()
        products_on_current_page = all_products[(page - 1) * 5:page * 5]

        for product in products_on_current_page:
            print(f"{product.id}. {product.name}, price: {product.price} in {product.category} category.")
        print(f"Page {page}/{total_pages}\n")

        if page in range(2, total_pages):
            next_or_previous = input("[n/p]|q for quit: ").lower()
            if next_or_previous == "n":
                page += 1
            elif next_or_previous == "p":
                page -= 1
            elif next_or_previous == "q":
                break
            else:
                continue

        elif page == 1:
            next_or_previous = input("[n]|q for quit: ").lower()
            if next_or_previous == "n":
                page += 1
            elif next_or_previous == "q":
                break
            else:
                continue

        elif page == total_pages:
            next_or_previous = input("[p]|q for quit: ").lower()
            if next_or_previous == "p":
                page -= 1
            elif next_or_previous == "q":
                break
            else:
                continue


@apply_tax
def show_basket(basket: Basket) -> str:
    """Return a string representation of the shopping items list."""
    result = "This is your basket:"
    if len(basket) == 0:
        result += "\nYou have nothing in your basket! Type and Enter add for adding some products."
    for item in basket:
        result += f"\n-{item['name']}: {item['unit']} in your basket, price: {item['price']}, category: {item['category']}."

    return result


def title_and_strip_items(items: ProductNames) -> ProductNames:
    """Converts all items in the list to title case and removes whitespaces from the the start and end of the items and returns the updated list."""
    items = list(map(str.title, items))
    items = list(map(str.strip, items))

    return items


def show_divider() -> str:
    """Return a string representing a divider."""
    return "--------"


def show_help() -> str:
    """
    Provide a help message with instructions for using the shopping store.

    Returns:
        str: The help message.
    """
    message = """
For viewing the products of the store please enter: products
For adding item(s) please enter: add
For removing item(s) please enter: remove
For editing an item please enter: edit
For searching the existence of your item please enter: search
For changing the priority of an item please enter: prioritize
To see how many products you have on your basket please enter: count
For showing your basket please enter: show
For returning back to the last step please enter: back
for showing this guideline again please enter: help
For finishing and quitting our store please enter: quit

ATTENTION: PUT ',' BETWEEN ITEMS WHEN ADDING OR REMOVING.
"""
    logger.debug("User viewed help successfully.")

    return message


def guide_message() -> str:
    """Return a guide message for commands."""
    message = "\nEnter help to see a guide for commands."
    return message


def clear_screen() -> NoReturn:
    """Clear the screen."""
    os.system("cls" if os.name == "nt" else "clear")
