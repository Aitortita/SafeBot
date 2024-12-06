import os
from logging.config import dictConfig
from dotenv import load_dotenv
import colorlog

load_dotenv()

DISCORD_API_TOKEN: str = os.getenv("DISCORD_API_TOKEN")
VIRUSTOTAL_API_KEY: str = os.getenv("VIRUSTOTAL_API_KEY")
DBHOST: str = os.getenv("DBHOST")
DBUSER: str = os.getenv("DBUSER")
DBPASSWORD: str = os.getenv("DBPASSWORD")
DBPORT: str = os.getenv("DBPORT")
DBNAME: str = os.getenv("DBNAME")

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "standard": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(levelname)s - %(asctime)s - %(name)s : %(message)s",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "white",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red"
            }
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": "logs/infos.log",
            "mode": "w"
        },
        "scan": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": "logs/scans.log",
            "mode": "w"
        }
    },
    "loggers": {
        "scans": {
            "handlers": ["console", "file", "scan"],
            "level": "INFO",
            "propagate": False
        },
        "bot": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        "discord": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        "sqlalchemy.engine": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

dictConfig(LOGGING_CONFIG)