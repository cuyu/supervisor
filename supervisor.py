'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 2/16/16
'''
import SocketServer
import socket
import sys

import time
from connection import Connection


global SERVER


class SuperManager(object):
    interrupted = False


class SuperRequestHandler(SocketServer.DatagramRequestHandler):
    def handle(self):
        msg = self.rfile.getvalue()
        if msg == 'still alive\n':
            SERVER.update_client_heartbeat(self.client_address, time.time())


class Supervisor(object):
    def __init__(self, host, port):
        """
        Bind `handle' method of SuperRequestHandler to handle requests from TCPServer.
        """
        self.host = host
        self.port = port
        self.server = SocketServer.UDPServer((host, port), SuperRequestHandler)
        self._client_heartbeat = {}

    def start_server(self):
        """
        Start a UDPServer to receive heartbeat of monitored clients.
        """
        while True:
            if SuperManager.interrupted:
                break
            self.server.handle_request()
        # print "OK, STOP!!!!!"
        # self.server.shutdown()
        # print "stopped"
        SuperManager.server_stopped = True

    def setup_client(self, host, port, user, password):
        """
        Used to download client server code to the client and start the server on the client.
        """
        pass

    def connect_client(self, host, port=51000):
        """
        Used to set up the communication between a running client and the supervisor.
        """
        con = Connection(host, port, 'TCP')
        con.send_cmd('startheartbeat', self.host, self.port)
        con.close()

    def update_client_heartbeat(self, client_address, beat_time):
        print client_address, '@', beat_time
        self._client_heartbeat[client_address[0]] = beat_time


if __name__ == "__main__":
    HOST, PORT = socket.gethostname(), 52000
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    # Create the server, binding to HOST on port PORT
    SERVER = Supervisor(HOST, PORT)
    # Activate the server; this will keep running until you
    # interrupt with ClientManager.interrupted = True
    SERVER.start_server()
