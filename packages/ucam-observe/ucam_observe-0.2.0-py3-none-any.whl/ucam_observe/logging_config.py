import logging
import os
import re
from logging.config import dictConfig

import structlog


def get_log_level_name():
    """Retrieve log level from environment variables."""
    VALID_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    input_upper = os.getenv("LOG_LEVEL", "INFO").upper()

    if input_upper not in VALID_LEVELS:
        raise RuntimeError(f"{input_upper} not from valid choices {VALID_LEVELS}")

    return input_upper


def get_log_level_int():
    return logging.getLevelName(get_log_level_name())


def get_console_logging_status():
    """Retrieve console logging status from environment variables."""
    return os.getenv("CONSOLE_LOGGING", "False").lower() in ("true", "1")


def get_chosen_formatter_key():
    return "developer_console" if get_console_logging_status() else "json"


def get_chosen_handler_keys():
    return [get_chosen_formatter_key()]


def _add_gcp_log_severity(logger, method_name, event_dict):  # pragma: no cover
    """
    Add the log level to the event dict under the "severity" key.

    This is used as a structlog log processor, and is necessary as severity is used by GCP instead
    of level.

    Based on the structlog.stdlib.add_log_level processor.
    """
    if method_name == "warn":
        method_name = "warning"
    event_dict["severity"] = method_name
    return event_dict


# From https://albersdevelopment.net/2019/08/15/using-structlog-with-gunicorn/
def _gunicorn_combined_logformat(logger, name, event_dict):
    if event_dict.get("logger") == "gunicorn.access":
        try:
            message = event_dict["event"]

            parts = [
                r"(?P<host>\S+)",  # host %h
                r"\S+",  # indent %l (unused)
                r"(?P<user>\S+)",  # user %u
                r"\[(?P<time>.+)\]",  # time %t
                r'"(?P<request>.+)"',  # request "%r"
                r"(?P<status>[0-9]+)",  # status %>s
                r"(?P<size>\S+)",  # size %b (careful, can be '-')
                r'"(?P<referer>.*)"',  # referer "%{Referer}i"
                r'"(?P<agent>.*)"',  # user agent "%{User-agent}i"
            ]
            pattern = re.compile(r"\s+".join(parts) + r"\s*\Z")
            m = pattern.match(message)
            res = m.groupdict()

            if res["user"] == "-":
                res["user"] = None

            res["status"] = int(res["status"])

            if res["size"] == "-":
                res["size"] = 0
            else:
                res["size"] = int(res["size"])

            if res["referer"] == "-":
                res["referer"] = None

            event_dict.update(res)

        # We want the log even if this code fails
        except:  # noqa E722 rare occasion where we do want to carry on if this block fails
            pass

    return event_dict


def get_common_structlog_processors():
    # This configuration is used by logs that originate from both standard python loggers and
    # structlog loggers
    return [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        _add_gcp_log_severity,
        _gunicorn_combined_logformat,
        structlog.processors.CallsiteParameterAdder(
            {
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.PROCESS,
                structlog.processors.CallsiteParameter.THREAD,
            }
        ),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]


def get_dict_config_formatters():
    return {
        "developer_console": {
            "()": "structlog.stdlib.ProcessorFormatter",
            "processor": structlog.dev.ConsoleRenderer(colors=True),
            "foreign_pre_chain": get_common_structlog_processors(),
        },
        "json": {
            "()": "structlog.stdlib.ProcessorFormatter",
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": get_common_structlog_processors(),
        },
    }


def get_dict_config_handlers():
    return {
        "developer_console": {
            "class": "logging.StreamHandler",
            "formatter": "developer_console",
        },
        "json": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    }


def get_dict_config():
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": get_dict_config_formatters(),
        "handlers": get_dict_config_handlers(),
        "loggers": {
            # This is potentially overridden by gunicorn
            "": {
                "handlers": get_chosen_handler_keys(),
                "level": get_log_level_name(),
            },
        },
    }


def configure_structlog():
    # This configuration is just used by logs that are generated by structlog loggers
    structlog.configure(
        processors=[
            *get_common_structlog_processors(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(get_log_level_int()),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def configure_logging(force_reset=False):
    """Configure structured logging for both Python logging and structlog."""

    global configure_logging_run
    if not force_reset and configure_logging_run:
        return

    configure_logging_run = True

    dictConfig(get_dict_config())

    configure_structlog()


configure_logging_run = False
