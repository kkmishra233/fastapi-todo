import json
import logging
from core.config import settings
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(settings.PROJECT_TITLE)
logger.setLevel(logging.INFO)

# set formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

## add logger structure
class StructuredLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        if extra is None:
            extra = {}
        extra['app_name'] = settings.PROJECT_TITLE
        super()._log(level, json.dumps(msg) if isinstance(msg, dict) else msg, args, exc_info, extra, stack_info)
logging.setLoggerClass(StructuredLogger)

## configure handler
handler = RotatingFileHandler(settings.LOG_FILE, maxBytes=10000, backupCount=3)
file_handler = logging.FileHandler(settings.LOG_FILE)
stream_handler = logging.StreamHandler()
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# add handlers
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.addHandler(handler)
