import config
from server import GeoServer
from processor import Processor
import multiprocessing
import sys

host_ip = config.host_ip
host_port = config.host_port


def main():

    data_queue = multiprocessing.Queue()
    geo_server = GeoServer(host_ip, host_port, data_queue)
    processor = Processor(data_queue)
    consumer = multiprocessing.Process(target=processor.process_data)
    consumer.daemon = True
    consumer.start()
    try:
        geo_server.run_loop()
        consumer.join()
    except KeyboardInterrupt:
        geo_server.stop_loop()
        print("Bye")
        sys.exit(0)


if __name__ == '__main__':
    main()


