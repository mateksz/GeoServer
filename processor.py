from data_base import DataBase
import time
import sys
import logging

log = logging.getLogger(__name__)


class Processor:

    def __init__(self, data_queue):
        self.data_queue = data_queue
        self.data_base = DataBase()

    def process_data(self):
        try:
            while True:
                geo_data = self.data_queue.get()
                log.debug("Received data from queue")
                self.normalize_data(geo_data)
                log.debug("Witting data to the base...")
                self.data_base.write_data(geo_data)
                log.debug("Data writen")
        except KeyboardInterrupt:
            log.debug("Closing processor")
            sys.exit(0)


    def normalize_data(self, data):
        """Place holder for implementing additional data parsing"""
        time.sleep(2)
