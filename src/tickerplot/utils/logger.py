#
# Refer to LICENSE file and README file for licensing information.
#
"""
logging utilities
"""

import os
import time
from datetime import datetime as dt
import sys

import logging
_LOG_FILE = 'tickerplot.log'

_CONSOLE_LOG_LEVEL = logging.WARNING
_DEFAULT_LOG_LEVEL = logging.INFO

def get_logger(name=__name__, default_level=None,
                console_level=None, log_file=None):
    """
        Returns a Logger object with a given name adds two handlers -
        viz. Stream (console) and a File handler.
    """
    global _CONSOLE_LOG_LEVEL, _DEFAULT_LOG_LEVEL

    console_level = console_level or _CONSOLE_LOG_LEVEL
    default_level = default_level or _DEFAULT_LOG_LEVEL

    logger = logging.getLogger(name)
    logger.setLevel(min(default_level, console_level))

    ch = logging.StreamHandler()
    ch.setLevel(console_level)

    log_file = log_file or _LOG_FILE
    fh = logging.FileHandler(log_file)
    fh.setLevel(default_level)

    logger.addHandler(ch)
    logger.addHandler(fh)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    return logger

if __name__ == '__main__':
    pass
