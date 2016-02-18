'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 2/18/16
'''

# For test only
import time

from connection import Connection

if __name__ == "__main__":
    con = Connection("10.66.4.82", 52000, 'UDP')
    con.send('still alive')
    time.sleep(2)
    con.send('still alive')
    con.close()
