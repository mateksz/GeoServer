import config
from server import GeoServer
from processor import Processor
import multiprocessing
import sys
import logging

host_ip = config.host_ip
host_port = config.host_port
logfile = config.log_file
log_level = config.log_level
log_format = config.log_format
log_date_format = config.log_date_format

logging.basicConfig(
                    filename=logfile,
                    filemode='a',
                    format=log_format,
                    datefmt=log_date_format,
                    level=logging.DEBUG
                    )
log = logging.getLogger(__name__)


def main():

    data_queue = multiprocessing.Queue()
    geo_server = GeoServer(host_ip, host_port, data_queue)
    processor = Processor(data_queue)
    processor_p = multiprocessing.Process(target=processor.process_data, name='processor')
    processor_p.daemon = True
    processor_p.start()
    try:
        log.info('Geo server app starting...')
        geo_server.run_loop()
        processor_p.join()
        log.info('Geo server app start completed')
    except KeyboardInterrupt:
        log.info('Received interrupt. Shutting down...')
        geo_server.stop_loop()
        log.info('Shutdown completed')
        sys.exit(0)


if __name__ == '__main__':
    main()


