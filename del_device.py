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

id = "fb9dd02d-979a-4c71-9e92-ce390d1c74b1"

def add_device():
    token = get_token()

    api_path = "https://sandboxdnac.cisco.com/dna"
    query = "?isForceDelete=false"
    headers ={"Content-type": "application/json", "X-Auth-Token" : token}

    # POST request to add a new device with device details from
    # dictionary created earlier
    del_resp = requests.delete(
            f'{api_path}/intent/api/v1/network-device/{id}{query}',
            headers=headers
    )
    
    print (f'{api_path}/intent/api/v1/network-device/{id}{query}')

    if del_resp.ok:

        # Wait a few seconds as this is an aysnc process
        print(f"Request accepted: status code {del_resp.status_code}")
        time.sleep(10)

        # Query DNA center to GET the status of task (task url gotten from response to add)
        task_path = del_resp.json()["response"]["url"]
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
        print(f"Device addition failed with code {del_resp.status_code}")
        print(f"Failure body: {del_resp.text}")


def main():
    add_device()

if __name__ == "__main__":
    main()
