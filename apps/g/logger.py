import os
import logging
from dynaconf import settings

def get_logger():
    log_format = '【 %(levelname)s 】 %(asctime)s - file \"%(pathname)s\" - line: %(lineno)d - %(message)s '
    logger = logging.getLogger('ms')
    logger.setLevel(logging.DEBUG)
    logfile = os.path.join(settings.LOG_DIR, settings.LOG_FILE)
    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


# logger.exception(ex)
