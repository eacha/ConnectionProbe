import sys
import threading


class OutputModule:

    def __init__(self, output_file=sys.stdout):
        if output_file != sys.stdout:
            self.output_file = open(output_file, mode='w')
        else:
            self.output_file = output_file

        # Declare the mutex
        self.thread_lock = threading.Lock()