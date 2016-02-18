'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 2/17/16
'''

# For test only
from control import Connection

if __name__ == "__main__":
    con = Connection("10.66.4.82")
    con.send('hello!!')
    con.close()
