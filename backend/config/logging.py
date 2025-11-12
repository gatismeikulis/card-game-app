import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[{asctime}] {levelname} {name} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        # Game package - only errors
        "game": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        # Silence Daphne DEBUG logs
        "daphne": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}
