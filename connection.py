'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 2/17/16
'''
import socket

COMMANDS = ['stopcontrol', 'startheartbeat']


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
        sock = self._connect()
        sock.send(message + '\n')

    def send_cmd(self, cmd, args):
        """
        :param cmd: should be a cmd listed in COMMANDS.
        :param args: is a list contains a set of messages. (each message send as a line)
        e.g. send('addsupervisor', ['systest-auto-master', '51000'])
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
