'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 2/17/16
'''
import socket

# Supported commands for controlling clients:
# [0]stopcontrol -- stop the server
# [1]startheartbeat -- start to send heartbeat messages
# [2]execute -- execute system command on local machine
COMMANDS = ['stopserver', 'startheartbeat', 'execute']


class Connection(object):
    def __init__(self, host, port, connect_type='TCP'):
        self.host = host
        self.port = port
        self.connect_type = connect_type.upper()

    def _connect(self):
        if self.connect_type == 'TCP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.connect_type == 'UDP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            raise Exception('Connection type unknown: {0}'.format(self.connect_type))
        sock.connect((self.host, self.port))
        return sock

    def send(self, message):
        """
        Send a message.
        """
        sock = self._connect()
        sock.send(message + '\n')

    def send_cmd(self, cmd, *args):
        """
        Send command. (Usually used for supervisor send to clients)
        :param cmd: should be a cmd listed in COMMANDS.
        :param args: a set of argument messages. (each message send as a line)
        e.g. send('addsupervisor', 'systest-auto-master', '51000')
        """
        sock = self._connect()
        sock.send(self.get_short_cmd(cmd) + '\n')
        for msg in args:
            sock.send(msg + '\n')
        sock.send('$$$\n')  # Send this line as ending flag.

    def close(self):
        pass

    def get_short_cmd(self, longcmd):
        """
        Transform command to short number for efficient.
        """
        longcmd = longcmd.lower()
        assert longcmd in COMMANDS, 'Unknown command: {0}'.format(longcmd)
        return str(COMMANDS.index(longcmd))
