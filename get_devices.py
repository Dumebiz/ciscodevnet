#!/usr/bin/env python

"""
Author: Dumebi Umezinne
Purpose: Demonstrate Python "requests" to get an access token
from Cisco DNA Center using the REST API.
"""

import requests
from auth_token import get_token
from rich import print
from dnacentersdk import api    


def get_devices():
    token = get_token()
    dnac = api.DNACenterAPI(
        base_url="https://sandboxdnac.cisco.com",
        username="devnetuser",
        password="Cisco123!",
    )
    
    devices = dnac.devices.get_device_list()

    print(devices)


    #import json
    #print(json.dumps(get_resp.json(), indent=2))
    #if get_resp.ok:
    for device in devices['response']:
        print(f"{device['id']}   IP: {device['managementIpAddress']}")
    
 #else:
 #       print(f'Device collection failed with code {get_resp.status_code}')
  #      print(f'Failure body: {get_resp.text}') """




def main():
    get_devices()

if __name__ == "__main__":
    main()
