import os
import logging
from logging import config

from core import settings

from .logger_config import logger_config

logs_dir = os.path.join(settings.project_directory, "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

config.dictConfig(logger_config)
logger = logging.getLogger("debug" if settings.debug else "main")

