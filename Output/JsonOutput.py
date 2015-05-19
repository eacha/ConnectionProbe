import json
import sys
from Output.OutputModule import OutputModule


class JsonOutput(OutputModule):

    def __init__(self, output_file=sys.stdout):
        OutputModule.__init__(self, output_file=output_file)

        self.first_object = True
        self.output_file.write('[\n')

    def write_dict(self, dict):
        self.thread_lock.acquire()
        if self.first_object:
            self.first_object = False
            self.output_file.write(json.dumps(dict))
        else:
            self.output_file.write(',\n' + json.dumps(dict))
        self.thread_lock.release()

    def close(self):
        self.output_file.write(']')



