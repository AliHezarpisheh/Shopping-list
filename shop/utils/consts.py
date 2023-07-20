from shop.handlers import (
    handle_add_command,
    handle_remove_command,
    handle_search_command,
    handle_change_index,
    handle_count_command,
)

COMMANDS = {
    "add": handle_add_command,
    "remove": handle_remove_command,
    "prioritize": handle_change_index,
    "count": handle_count_command,
    "search": handle_search_command,
}
