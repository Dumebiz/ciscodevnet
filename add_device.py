#!/usr/bin/env python

"""
Author: Dumebi Umezinne
Purpose: Demonstrate Python "requests" to get an access token
from Cisco DNA Center using the REST API.
"""

import requests
from auth_token import get_token
import time
import json
from pprint import pprint as pprint

new_device_dict = {
    "ipAddress": ["172.20.20.20"],
    "snmpVersion": "v3",
    "snmpROCommunity": "readonly",
    "snmpRWCommunity": "readwrite",
    "snmpRetry": "1",
    "snmpAuthPassphrase": "kjdiDI89",
    "snmpAuthProtocol": "",
    "snmpMode": "AUTHPRIV",
    "snmpPrivPassphrase": "hjdahDue88299",
    "snmpTimeout": "120",
    "snmpUserName": "admin",
    "cliTransport": "ssh",
    "userName": "ambrana",
    "password": "diablo419!",
    "enablePassword": "diavolo678!"
}

def add_device():
    token = get_token()

    api_path = "https://sandboxdnac.cisco.com/dna"
    headers ={"Content-type": "application/json", "X-Auth-Token" : token}

    # POST request to add a new device with device details from
    # dictionary created earlier
    add_resp = requests.post(
            f'{api_path}/intent/api/v1/network-device',
            json=new_device_dict,
            headers=headers
    )

    print(add_resp.status_code)
    #print(add_resp)
    #add_data = add_resp.json()
    #print(add_data)
    #print(add_resp.json()["response"])
    #print(add_resp.headers)
    print("***********************")
    

    if add_resp.ok:

        # Wait a few seconds as this is an aysnc process
        print(f"Request accepted: status code {add_resp.status_code}")
        time.sleep(10)

        # Query DNA center to GET the status of task (task url gotten from response to add)
        task_path = add_resp.json()["response"]["url"]
        print(f'{api_path}/intent{task_path}')
        task_resp = requests.get (
            f'{api_path}/intent{task_path}',
            headers = headers
        )        

        #Check if task GET is successful
        if task_resp.ok:

           task_data = task_resp.json()["response"]

           #Check if device add async task completed successfully
           if not task_data["isError"]:
               print("Successfully added new device")
           else:
               print(f"Async task error see: {task_data['progress']}")
               print(f"Aysnc task failure: {task_data['failureReason']}")
        
        else:
            print(f'Async GET failed: status code {task_resp.status_code}')
    
    else:
        #The initial new device POST failed with details below
        print(f"Device addition failed with code {add_resp.status_code}")
        print(f"Failure body: {add_resp.text}")


def main():
    add_device()

if __name__ == "__main__":
    main()
