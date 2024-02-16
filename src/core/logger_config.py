import os

from core import settings

logger_config = {
    "version": 1,
    "formatters": {
        "console": {
            "format": "%(levelname)s - %(module)s:%(filename)s:%(lineno)s - %(message)s"
        },
        "file": {
            "format": (
                "%(asctime)s - %(levelname)s - "
                "%(module)s:%(filename)s:%(lineno)s - %(message)s"
            )
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "console",
        },
        "debug_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "file",
            "filename": os.path.join(settings.project_directory, "logs", "debug.log"),
            "mode": "a",
            "maxBytes": 1048576,
            "backupCount": 5,
        },
        "union_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "file",
            "filename": os.path.join(settings.project_directory, "logs", "union.log"),
            "mode": "a",
            "maxBytes": 5242880,
            "backupCount": 10,
        },
        "error_file": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "file",
            "filename": os.path.join(settings.project_directory, "logs", "error.log"),
            "mode": "a",
        },
    },
    "loggers": {
        "": {"level": "NOTSET", "handlers": ["console", "debug_file", "union_file"]},
        "debug": {
            "level": "DEBUG",
            "handlers": ["console", "debug_file"],
            "propagate": False,
        },
        "main": {
            "level": "INFO",
            "handlers": ["union_file", "error_file"],
            "propagate": False,
        },
    },
}
