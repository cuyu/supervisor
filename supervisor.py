'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 2/16/16
'''
import SocketServer


class SuperRequestHandler(object):
    pass


class Supervisor(object):
    def __init__(self, host, port, interval=5):
        """
        Bind `handle' method of SuperRequestHandler to handle requests from TCPServer.
        """
        self.host = host
        self.port = port
        self.server = SocketServer.UDPServer((host, port), SuperRequestHandler)

    def start_server(self):
        """
        Start a UDPServer to receive heartbeat of monitored clients.
        """
        pass

    def add_client(self, host, port=51000):
        pass
