import config
import logging

dummy_file = config.dummy_file
log = logging.getLogger(__name__)

class DataBase:
    def write_data(self, geo_data):
        with open(dummy_file, 'a') as f:
            f.write(geo_data)