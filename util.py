__author__ = 'eduardo'

from os import path


def get_logging_config():
    return path.join(path.split(__file__)[0], 'logging.ini')