class DataBase:
    def write_data(self, geo_data):
        with open('/home/mateusz/base.txt', 'a') as f:
            f.write(geo_data)