import logging
import logging.config
import sys
import threading
import time
from util import get_logging_config

logging.config.fileConfig(get_logging_config())
logger = logging.getLogger(__name__)

TICKS = 2


class InputModule:

    def __init__(self, input_file=sys.stdin):
        if input_file != sys.stdin:
            self.input_file = open(input_file, mode='r')
        else:
            self.input_file = input_file

        # Declare the mutex
        self.thread_lock = threading.Lock()
        self.input_lines = 0

    def logging_ticks(self):
        if self.input_lines % TICKS == 0:
            logger.info('%s Lines processed %d', time.strftime('%H:%M:%S'), self.input_lines)