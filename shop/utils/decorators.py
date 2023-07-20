import functools
from typing import Callable, Tuple


def apply_tax(func: Callable) -> Callable:
    """Decorator that applies a 9% tax to the final price returned by the decorated function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.

    Example:
        @apply_tax
        def calculate_total_price(items):
            # Calculate the total price logic...

        total_price, final_price_with_tax = calculate_total_price(items)
    """
    @functools.wraps(func)
    def wrapped_func(basket) -> Tuple[str, float]:
        value = func(basket)

        float_prices = map(
            lambda item: float(item["price"].replace("$", "")) * item["unit"], basket.basket
        )
        price_after_tax = map(lambda price: price * 1.09, float_prices)
        final_price = sum(price_after_tax)

        return value, final_price

    return wrapped_func
