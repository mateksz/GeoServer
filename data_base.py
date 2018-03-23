import logging
import config

dummy_file = config.dummy_file


class DataBase:
    def write_data(self, geo_data):
        with open(dummy_file, 'a') as f:
            f.write(geo_data)