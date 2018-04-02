import config
from server import GeoServer
from processor import Processor
import logging
import logging.handlers
import multiprocessing
import sys


def main():
    """Entry point for the app

       Initializes logging according to the config file.
       Starts TCP socket server in one process and data
       processor in the other. Both processes share a queue.
       Server writes data to it and processor reads it. Due to
       multiprocessing complication, the app is meant to be shutdown with SIGINT.
    """
    try:
        log_file_handler = logging.handlers.RotatingFileHandler(config.log_file,
                                                                maxBytes=config.log_file_size * 1024 * 1024,
                                                                backupCount=config.log_file_backup)
    except Exception as e:
        print("FATAL. Unable to register log file : {}".format(e))
        sys.exit(1)
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
        root.info('Geo server app start completed') #TODO never displayed, due to multiprocessing/logging?
    except KeyboardInterrupt:
        root.info('Received interrupt. Shutting down...')
        geo_server.stop_loop()
        root.info('Shutdown completed')
        sys.exit(0)


if __name__ == '__main__':
    main()


