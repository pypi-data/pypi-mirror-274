from ucam_observe.logging_config import (
    get_chosen_formatter_key,
    get_chosen_handler_keys,
    get_dict_config_formatters,
    get_dict_config_handlers,
    get_log_level_name,
)

logconfig_dict = {
    "formatters": get_dict_config_formatters(),
    "root": {
        "handlers": get_chosen_handler_keys(),
        "level": get_log_level_name(),
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": get_chosen_formatter_key(),
            "stream": "ext://sys.stdout",
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": get_chosen_formatter_key(),
            "stream": "ext://sys.stderr",
        },
        **get_dict_config_handlers(),
    },
    "loggers": {
        "gunicorn.error": {
            "level": get_log_level_name(),
            "handlers": ["error_console"],
            # Whilst True is the default in CONFIG_DEFAULTS within structlog, these default
            # settings cause duplicate logs (the default settings are only applied when
            # logconfig_dict is specified and is not empty), presumably because other
            # settings cause gunicorn to programmatically add stdout/err to these existing
            # handlers.
            "propagate": False,
            "qualname": "gunicorn.error",
        },
        "gunicorn.access": {
            "level": get_log_level_name(),
            "handlers": ["console"],
            "propagate": False,
            "qualname": "gunicorn.access",
        },
    },
}
