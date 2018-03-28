import config
from server import GeoServer
from processor import Processor
import logging
import logging.handlers
import multiprocessing
import sys


def main():

    log_file_handler = logging.handlers.RotatingFileHandler(config.log_file,
                                                            maxBytes=config.log_file_size * 1024 * 1024,
                                                            backupCount=config.log_file_backup)
    log_file_handler.setLevel(config.log_level)
    log_file_handler.setFormatter(logging.Formatter(config.log_format, config.log_date_format))
    root = logging.getLogger()
    root.addHandler(log_file_handler)
    root.setLevel(logging.DEBUG)

    data_queue = multiprocessing.Queue()
    geo_server = GeoServer(config.host_ip, config.host_port, data_queue)
    processor = Processor(data_queue)
    processor_p = multiprocessing.Process(target=processor.process_data, name='processor')
    processor_p.daemon = True
    processor_p.start()

    try:
        root.info('Geo server app starting...')
        geo_server.run_loop()
        processor_p.join()
        root.info('Geo server app start completed')
    except KeyboardInterrupt:
        root.info('Received interrupt. Shutting down...')
        geo_server.stop_loop()
        root.info('Shutdown completed')
        sys.exit(0)


if __name__ == '__main__':
    main()


