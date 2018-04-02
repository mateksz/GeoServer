#Defaults to the all interface binding
host_ip = ''
host_port = 8888

#Socket timeout in seconds
client_time_out = 60

#For dummy database simulation
dummy_file = '/home/mateusz/base.txt'

#Logging, for reference see python docs
log_file = '/home/mateusz/geo_server.log'
log_file_size = 500 #In MegaBytes
log_file_backup = 10 #Number of copies in the filesystem
log_level = 'DEBUG'
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
log_date_format = '%Y-%m-%d %H:%M:%S'
