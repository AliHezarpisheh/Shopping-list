import logging
import tomllib
from pathlib import Path
from config.helpers.exceptions import ConfigFileError
from config.helpers.type_hint import MainLogConfig

# Reading the logging config file.
directory = Path.cwd()
log_config_path = directory / "config" / "log_config.toml"

with log_config_path.open(mode="rb") as toml_file:
    log_config: MainLogConfig = tomllib.load(toml_file)


# Extracting logger configs.
logger_config = log_config.get("logger", {}).get("root", {})

# Creating logger.
logger = logging.getLogger()
logger.setLevel(logger_config["level"])

# Creating handlers.
handler_names = logger_config.get("handlers", {})

for name in handler_names:
    handler_config = log_config.get("handler", {}).get(name, {})

    handler_class = handler_config["class"]
    if handler_class == "FileHandler":
        handler = logging.FileHandler(filename="shop.log", mode="a")
        handler.setLevel(handler_config["level"])

        # Set formatter.
        formatter_name = handler_config.get("formatter", {})
        formatter_config = log_config.get("formatter", {}).get(formatter_name, {})
        format = logging.Formatter(formatter_config["format"])
        handler.setFormatter(format)

        # Setting handlers.
        logger.addHandler(handler)
    else:
        raise ConfigFileError("No file handler has been set in config file.")


def config_logging() -> logging.Logger:
    """Return a logger with specified configurations."""
    return logger
