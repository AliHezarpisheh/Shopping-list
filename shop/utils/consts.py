from shop.handlers import (
    handle_add_command,
    handle_remove_command,
    handle_search_command,
    handle_change_index,
    handle_count_command
)

ASSIGN_COMMANDS = {
    "add": handle_add_command,
    "remove": handle_remove_command,
    "prioritize": handle_change_index,
}

NO_ASSIGN_COMMANDS = {
    "count": handle_count_command,
    "search": handle_search_command
}
