import config
import threading
import socketserver
import traceback
import logging

client_time_out = config.client_time_out
log = logging.getLogger(__name__)


class GeoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.request.settimeout(client_time_out)
        while True:
            data = str(self.request.recv(1024), 'ascii')
            if data[0] == "$":
                log.debug("Received data form {}".format(self.client_address[0]))
                self.server.data_queue.put(data)
                log.debug("Data put into queue")
            else:
                log.debug("Data malformed - dropping")
                self.request.close()
                break


class BaseGeoServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True

    def __init__(self, host_port_tuple, streamhandler, data_queue):
        super().__init__(host_port_tuple, streamhandler)
        self.data_queue = data_queue

    def handle_error(self, request, client_address):
        if "socket.timeout" in str(traceback.format_exc()):
            log.info("Time out from {}".format(client_address[0]))
        else:
            print('-'*40)
            print('Exception happened during processing of request from', end=' ')
            print(client_address)
            traceback.print_exc() # XXX But this goes to stderr!
            print('-'*40)


class GeoServer:

    def __init__(self, host_address, host_port, data_queue):
        self.geo_server = BaseGeoServer((host_address, host_port), GeoRequestHandler, data_queue)

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


















