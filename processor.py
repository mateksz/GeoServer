from data_base import DataBase
import time
import sys
import logging

log = logging.getLogger(__name__)


class Processor:
    """Reads data from the queue and puts it to the database

       Work in progress:
        Needs to design data model.
        Decide on protocols being supported.
       Shutdowns on SIGINT that is send from the main function.
    """

    def __init__(self, data_queue):
        self.data_queue = data_queue
        self.data_base = DataBase()

    def process_data(self):
        try:
            while True:
                geo_data = self.data_queue.get()
                log.debug("Received data from queue")
                self.normalize_data(geo_data)
                log.debug("Writing data to the base...")
                self.data_base.write_data(geo_data)
                log.debug("Data writen")
        except KeyboardInterrupt:
            log.debug("Closing processor")
            sys.exit(0)


    def normalize_data(self, data):
        """Place holder for implementing additional data parsing"""
        time.sleep(2)
