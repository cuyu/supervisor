'''_
@author: Curtis Yu
@contact: cuyu@splunk.com
@since: 2/19/16
'''
import requests

if __name__ == "__main__":
    address = 'http://10.66.4.82:12000'
    r = requests.get(address)
    r = requests.post(address, data={'key': 'value'})
