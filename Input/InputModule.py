import sys


class InputModule:

    def __init__(self, input_file=sys.stdin):
        if input_file != sys.stdin:
            self.input_file = open(input_file, mode='r')
        else:
            self.input_file = input_file