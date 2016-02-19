'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 2/17/16
'''

# For test only
from connection import Connection

if __name__ == "__main__":
    con = Connection("10.66.129.97", 51000, 'TCP')
    con.send_cmd('stopserver')
    # con.send_cmd('startheartbeat', '10.66.4.82', '52000')
    # con.send_cmd('execute', '/Applications/splunk/bin/splunk version')
    con.close()
