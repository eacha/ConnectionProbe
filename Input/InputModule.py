import logging
import sys
import threading

logger = logging.getLogger('Input.InputModule')
logging.basicConfig(level=logging.DEBUG)
TICKS = 500


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
        if self.input_line % TICKS:
            logger.info('Lines processed %d', self.input_lines)