'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 2/17/16
'''
import SocketServer
import socket
import sys

import time
from control import Connection, COMMANDS

# Set socket timeout to avoid handle_request blocking.
socket.setdefaulttimeout(5)


class ClientManager(object):
    """
    Used as global signals.
    """
    interrupted = False  # if the SCS shall be interrupted: set true


class ClientExecutor(object):
    """
    Use this class to execute commands on the client machine.
    """

    def __init__(self):
        pass

    def execute(self, cmd, args):
        cmd = COMMANDS[cmd]
        if cmd == 1:
            # TODO: how to bind `server' to the specific client server
            server.add_supervisor(*args)


class ClientRequestHandler(SocketServer.StreamRequestHandler):
    """
    Just override the handle method to handle our requests.
    """

    def handle(self):
        cmd = self.rfile.readline().strip()
        msg = ''
        args = []
        while msg != '$$$':
            msg = self.rfile.readline().strip()
            args.append(msg)
        executor = ClientExecutor()
        result = executor.execute(cmd, args)


class ClientServer(object):
    """
    Use this class to start a TCPServer and listen for requests in a loop.
    """

    def __init__(self, host, port, interval=5):
        """
        Bind `handle' method of SuperRequestHandler to handle requests from TCPServer.
        """
        self.host = host
        self.port = port
        self.server = SocketServer.TCPServer((host, port), ClientRequestHandler)
        self.interval = interval
        self.supervisor = None

    def start_server(self):
        """
        Starts the server like TCPServer.serve_forever,
        but shuts down on interrupt.
        Send a heart beat to supervisor1 server in a given interval.
        """
        last_time = 0
        while True:
            if ClientManager.interrupted:
                break
            self.server.handle_request()
            this_time = time.time()
            if this_time > last_time + self.interval:
                last_time = this_time
                if not self.supervisor:
                    self.supervisor.send("i'm alive")
        # print "OK, STOP!!!!!"
        # self.server.shutdown()
        # print "stopped"
        ClientManager.server_stopped = True

    def add_supervisor(self, host, port):
        """
        This method should be called from handle_request().
        """
        self.supervisor = Connection(host, port)


if __name__ == "__main__":
    HOST, PORT = socket.gethostname(), 51000
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    # Create the server, binding to HOST on port PORT
    server = ClientServer(HOST, PORT)
    # Activate the server; this will keep running until you
    # interrupt with ClientManager.interrupted = True
    server.start_server()
