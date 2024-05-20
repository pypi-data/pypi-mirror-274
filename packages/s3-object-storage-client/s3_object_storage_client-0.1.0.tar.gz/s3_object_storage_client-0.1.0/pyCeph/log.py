'''
@File    :   logger.py
@Time    :   2022/07/11 17:34:49
@Author  :   susufqx
@Version :   1.0
@Contact :   jiangsulirui@gmail.com
'''

import sys
import logging
import traceback


LOGGING_CONFIG = dict(
    version=1,
    disable_existing_loggers=False,

    loggers={
        "s3": {
            "level": "INFO",
            "handlers": ["console"]
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout
        }
    },
    formatters={
        "generic": {
            "format": "%(asctime)s - (%(name)s) [%(levelname)s] %(process)d %(filename)s:%(lineno)d | %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        }
    }
)

logger = logging.getLogger('s3')


def print_excp(e: Exception, info=''):
    tb = traceback.format_tb(e.__traceback__, 20)
    logger.error(f"{str(e)} {info}\n{''.join(tb)}")
