import os
from logging.config import dictConfig
from dotenv import load_dotenv

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
    "disabled_existing_Loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers": {
        "console": {
            'level': "DEBUG",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "console2": {
            'level': "DEBUG",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "file": {
            'level': "DEBUG",
            'class': "logging.FileHandler",
            'filename': "logs/infos.log",
            'mode': "w"
        },
    },
    "loggers": {
        "bot": {
            'handlers': ['console'],
            'level': "INFO",
            "propagate": False
        },
        "discord": {
            'handlers': ['console2', "file"],
            "level": "INFO",
            "propagate": False
        }
    }
}

dictConfig(LOGGING_CONFIG)