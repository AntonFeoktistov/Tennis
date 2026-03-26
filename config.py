import os
import logging
import sys


class Config:

    HOST = os.getenv("HOST", "localhost")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def setup_logging(cls):
        level = getattr(logging, cls.LOG_LEVEL, logging.INFO)

        logging.basicConfig(
            level=level,
            format=cls.LOG_FORMAT,
            datefmt=cls.LOG_DATE_FORMAT,
            handlers=[logging.StreamHandler(sys.stdout)],
        )

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        return logging.getLogger(name)
