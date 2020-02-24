import logging
import os

from dynaconf import settings


def get_logger():
    log_format = '【 %(levelname)s 】 %(asctime)s - file \"%(pathname)s\"\
         - line: %(lineno)d - %(message)s '
    logger = logging.getLogger('ms')
    logger.setLevel(logging.DEBUG)
    log_dir = settings.get('log_dir', '/tmp')
    log_file = settings.get('log_file', 'ms.log')
    logfile = os.path.join(log_dir, log_file)
    fh = logging.FileHandler(logfile)
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
