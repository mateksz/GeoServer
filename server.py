import config
import threading
import socketserver
import traceback
import logging
import sys


log = logging.getLogger(__name__)


class GeoRequestHandler(socketserver.BaseRequestHandler):
    """Implements request handler

        No application layer protocol, just bytes send over TCP socket.
        Accepts any data, that meets basic requirements. No session control/retransmission
        or closing. Server closes socket on the preconfigured timeout. Keeps track of
        received packages. Writes data to the multiprocessing data queue, from where data
        processor reads.
    """
    def handle(self):
        self.request.settimeout(config.client_time_out)
        counter = 0
        while True:
            data = str(self.request.recv(1024), 'ascii')
            if data[0] == "$":
                log.debug("Received package number {0} from {1}".format(counter + 1, self.client_address[0]))
                if counter == 0:
                    log.info("Received first package from {}".format(self.client_address[0]))
                self.server.data_queue.put(data) #TODO research into problems & error handling
                log.debug("Data put into queue")
                counter += 1
            else:
                log.debug("Data malformed - dropping")
                self.request.close()
                break


class BaseGeoServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Defines application server as a basic TCP socket server

        Sets threads to deamon mode, so spawned sockets are closed as soon as the main thread is closing.
        Overrides __init__, so we pass multiprocessing data queue, which is used in request handler.
        We log socket timeout as an info. We catch exceptions in threads and log them
        as errors with full stack trace.
    """
    daemon_threads = True

    def __init__(self, host_port_tuple, streamhandler, data_queue):
        super().__init__(host_port_tuple, streamhandler)
        self.data_queue = data_queue

    def handle_error(self, request, client_address):
        if "socket.timeout" in str(traceback.format_exc()):
            log.info("Time out from {}".format(client_address[0]))
        else:
            log.warning("Exception happened during processing of request from {}".format(client_address[0]))
            log.exception("Exception : ")


class GeoServer:
    """App class to be initialized as a TCP socket server"""

    def __init__(self, host_address, host_port, data_queue):
        #Takes queue so it is passed to TCP server, where handler uses it
        try:
            self.geo_server = BaseGeoServer((host_address, host_port), GeoRequestHandler, data_queue)
        except Exception as e:
            log.fatal("Unable to initialize main server thread {}".format(e))
            sys.exit(1)

    def run_loop(self):
        server_thread = threading.Thread(target=self.geo_server.serve_forever)
        server_thread.daemon = True
        log.debug("Starting main server thread...")
        server_thread.start()
        log.debug("Started main server thread")

    def stop_loop(self):
        log.debug("Shutting down main loop...")
        self.geo_server.shutdown()
        self.geo_server.server_close()
        log.debug("Server main loop shut down completed")


















