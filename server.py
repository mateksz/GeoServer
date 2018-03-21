import config
import threading
import socketserver
import traceback
import sys

client_time_out = config.client_time_out


class GeoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.request.settimeout(client_time_out)
        try:
            while True:
                data = str(self.request.recv(1024), 'ascii')
                if data[0] == "$":
                    self.server.data_queue.put(data)
                else:
                    self.request.close()
                    break
        except KeyboardInterrupt:
            print("Disconnecting {}".format(self.client_address))
            self.request.close()



class BaseGeoServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    def __init__(self, host_port_tuple, streamhandler, data_queue):
        super().__init__(host_port_tuple, streamhandler)
        self.data_queue = data_queue

    def handle_error(self, request, client_address):
        if "socket.timeout" in str(traceback.format_exc()):
            print("Time out from {}".format(client_address))
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
        server_thread.start()
        self.geo_server.shutdown()
        self.geo_server.server_close()

    def stop_loop(self):
        print("shutting down main loop...")
        self.geo_server.shutdown()
        self.geo_server.server_close()
        print("server main loop shut down completed")


















