from data_base import DataBase
import time
import sys


class Processor:

    def __init__(self, data_queue):
        self.data_queue = data_queue
        self.data_base = DataBase()

    def process_data(self):
        try:
            while True:
                geo_data = self.data_queue.get()
                self.normalize_data(geo_data)
                self.data_base.write_data(geo_data)
        except KeyboardInterrupt:
            print("Closing processor")
            sys.exit(0)


    def normalize_data(self, data):
        """Place holder for implementing additional data parsing"""
        time.sleep(2)
