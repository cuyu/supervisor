'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 2/17/16
'''
import socket

COMMANDS = ['stopcontrol', 'startheartbeat']


class Connection(object):
    def __init__(self, host, port=51000):
        self.host = host
        self.port = port

    def send(self, messages):
        """
        :param messages: is a list contains a set of messages. (each message send as a line)
        e.g. send(['addsupervisor', 'systest-auto-master', '51000'])
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.send(self.get_short_cmd(messages[0]) + '\n')
        for msg in messages[1:]:
            sock.send(msg + '\n')
        sock.send('$$$\n')  # Send this line as ending flag.

    def close(self):
        pass

    def get_short_cmd(self, longcmd):
        """
        Transform command to short number for efficient.
        """
        longcmd = longcmd.lowercase()
        return str(COMMANDS.index(longcmd))
