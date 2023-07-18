import csv
from pathlib import Path
from collections import namedtuple
from typing import NamedTuple
from shop.utils.funcs import title_and_strip_items
from shop.helpers.exceptions import ProductFileDoesNotExist
from shop.helpers.type_hints import Products
from config.log_config import config_logging

logger = config_logging()

try:
    directory = Path.cwd()
    products_path = directory / "shop" / "models" / "products.csv"
    with open("shop/models/products.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        # Saving first line in column_names and discarding them in csv_reader.
        column_name = next(csv_reader)
        column_name = list(map(str.lower, column_name))

        # Defining a namedtuple with field names equivalent to column_names.
        BaseProduct: NamedTuple = namedtuple("BaseProduct", column_name, rename=True)

        class Product(BaseProduct):
            """
            This class represents a product.

            It is derived from the `BaseProduct` named tuple and provides additional functionality.

            Attributes:
                __slots__: Optimizes memory usage by eliminating the need for a dynamic dictionary for instance variables.

            Properties:
                float_price_without_sign (float): The price of the product without the dollar sign as a floating-point number.
            """
            __slots__ = ()

            @property
            def float_price_without_sign(self) -> float:
                removed_dollar_sing = self.price.replace("$", "")
                return float(removed_dollar_sing)

        # Storing products.
        all_products: Products = list()
        for row in csv_reader:
            row = title_and_strip_items(row)
            # Saving each line of the csv file in a namedtuple.
            try:
                product = Product(*row)
            except TypeError:
                logger.critical("One or more of the products parameters are more than the columns.")
                print("Error 500! Call the Administrator.")

            # Turn id and quantities to integers.
            product = product._replace(id=int(product.id))
            product = product._replace(quantity=int(product.quantity))
            all_products.append(product)
except FileExistsError:
    message = "Products file in shop/models had some troubles through opening and reading"
    logger.critical(message)
    raise ProductFileDoesNotExist(message)
else:
    logger.debug("Products have saved correctly.")


def get_all_products() -> Products:
    """Return all products."""
    return all_products
