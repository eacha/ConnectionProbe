import sys
import csv
from Input.InputModule import InputModule


class CSVInput(InputModule):
    CSV_DELIMITER = ','
    TSV_DELIMITER = '\t'

    def __init__(self, input_file=sys.stdin, delimiter=CSV_DELIMITER):
        InputModule.__init__(self, input_file=input_file)
        self.reader = csv.reader(self.input_file, delimiter=delimiter)

        try:
            self.columns_names = self.reader.next()
        except StopIteration:
            self.columns_names = list()

    def get_column_id(self, name):
        try:
            return self.columns_names.index(name)
        except ValueError:
            return 0

    def read(self):
        self.thread_lock.acquire()
        try:
            row = self.reader.next()
            self.input_lines += 1
            self.logging_ticks()
        except StopIteration:
            row = None
        self.thread_lock.release()

        return self.get_element(row, self.get_column_id('saddr'))

    def close(self):
        self.input_file.close()

    def get_element(self, list, index):
        if list is None:
            return None
        else:
            return list[index]