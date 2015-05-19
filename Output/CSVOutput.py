import csv
import sys
from Output.OutputModule import OutputModule


class CSVOutput(OutputModule):
    CSV_DELIMITER = ','
    TSV_DELIMITER = '\t'

    def __init__(self, delimiter=CSV_DELIMITER, output_file=sys.stdout):
        OutputModule.__init__(self, output_file=output_file)

        self.writer = csv.writer(self.output_file, delimiter=delimiter)
        self.printed_header = False

    def write_dict(self, dict):
        self.thread_lock.acquire()
        if not self.printed_header:
            self.printed_header = True
            self.writer.writerow(dict.keys())
        self.writer.writerow(dict.values())
        self.thread_lock.release()

    def close(self):
        self.output_file.close()
