'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 2/16/16
'''
import SocketServer
import socket
import SimpleHTTPServer
import time
import threading
from connection import Connection

global SERVER


class SuperManager(object):
    interrupted = False


class SuperHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    # Default is "HTTP/1.0"
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # The content of self.wfile is what we get after sending the http request.
        # In correspond, the content of self.rfile is what we send to the http request.
        # We do not need to parse it by our own as the SimpleHTTPRequestHandler.parse_request()
        # has done this job for us already.
        self.wfile.write("<html><body><h1>TODO</h1></body></html>")


class SuperUDPRequestHandler(SocketServer.DatagramRequestHandler):
    def handle(self):
        msg = self.rfile.getvalue()
        if msg == 'still alive\n':
            SERVER.update_client_heartbeat(self.client_address, time.time())


class Supervisor(object):
    def __init__(self, host):
        """
        Bind `handle' method of SuperRequestHandler to handle requests from TCPServer.
        """
        self.host = host
        # Port info will be init when starting corresponding server, cause we may just want to
        # use part of the features. (e.g. we may not need http server and use udp server only)
        self.udp_port = None
        self.http_port = None
        self._client_heartbeat = {}

    def start_udp_server(self, port):
        """
        Start a UDPServer to receive heartbeat of monitored clients.
        """
        self.udp_port = port
        udp_server = SocketServer.UDPServer((self.host, port), SuperUDPRequestHandler)
        while True:
            if SuperManager.interrupted:
                break
            udp_server.handle_request()
        # print "OK, STOP!!!!!"
        # self.server.shutdown()
        # print "stopped"
        SuperManager.server_stopped = True

    def start_http_server(self, port):
        self.http_port = port
        httpd = SocketServer.TCPServer((self.host, port), SuperHTTPRequestHandler)
        httpd.serve_forever()

    def setup_client(self, host, port, user, password):
        """
        Used to download client server code to the client and start the server on the client.
        """
        pass

    def connect_client(self, host, port=51000):
        """
        Used to set up the communication between a running client and the supervisor.
        """
        assert self.udp_port is not None
        con = Connection(host, port, 'TCP')
        con.send_cmd('startheartbeat', self.host, self.udp_port)
        con.close()

    def update_client_heartbeat(self, client_address, beat_time):
        print client_address, '@', beat_time
        self._client_heartbeat[client_address[0]] = beat_time


class FuncThread(threading.Thread):
    """
    Create a thread to run the input function with given args.
    The args should be a tuple or a list.
    """

    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        print 'Start thread on function: ' + self.func.__name__ + '\n'
        self.func(*self.args)


if __name__ == "__main__":
    HOST = socket.gethostname()
    UDP_PORT = 52000
    HTTP_PORT = 12000
    # Create the server, binding to HOST on port PORT
    SERVER = Supervisor(HOST)
    # Activate the server; this will keep running until you
    # interrupt with ClientManager.interrupted = True
    thread_udp_server = FuncThread(SERVER.start_udp_server, (UDP_PORT,))
    thread_http_server = FuncThread(SERVER.start_http_server, (HTTP_PORT,))

    thread_udp_server.start()
    thread_http_server.start()
