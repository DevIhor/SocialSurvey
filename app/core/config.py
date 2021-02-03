import logging
import sys

from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret, CommaSeparatedStrings

from app.core.logging import InterceptHandler

API_PREFIX = "/api"
JWT_TOKEN_PREFIX = "Token"
VERSION = "0.0.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)
DATABASE_URL: DatabaseUrl = config("DB_CONNECTION", cast=DatabaseUrl)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
PROJECT_NAME: str = config("PROJECT_NAME", default="Social Survey")
ALLOWED_HOSTS: list = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="")

# Logging configs
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging.getLogger(logger_name).handlers = [InterceptHandler(LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
