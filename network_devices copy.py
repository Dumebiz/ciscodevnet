import requests
import prettytable
from requests.auth import HTTPBasicAuth
import os
import sys
from rich import print

# Get the absolute path for the directory where this file is located "here"
here = os.path.abspath(os.path.dirname(__file__))

# Get the absolute path for the project / repository root
project_root = os.path.abspath(os.path.join(here, "../.."))

# Extend the system path to include the project root and import the env files
sys.path.insert(0, project_root)

import env_lab

DNAC = env_lab.DNA_CENTER["host"]
DNAC_username = env_lab.DNA_CENTER["username"]
DNAC_password = env_lab.DNA_CENTER["password"]
DNAC_port = env_lab.DNA_CENTER["port"]


def get_auth_token(controller_ip=DNAC, port=DNAC_port):
    """ Authenticates with controller and returns a token to be used in subsequent API
    invocations """

    login_url = f"https://{controller_ip}:{port}/dna/system/api/v1/auth/token"
    print(login_url)
    hdr = {"content-type": "application/json"}
    result = requests.post(url=login_url, auth=HTTPBasicAuth(DNAC_username, DNAC_password), verify=False,
    headers=hdr)
    
    result.raise_for_status()

    token = result.json()["Token"]
    #print(token)
    return {
        "controller_ip": controller_ip,
        "token": token
    }


def create_url(path, controller_ip=DNAC):
    """ Helper function to create a DNAC API endpoint url
    """
    #print(f'https://{controller_ip}:{DNAC_port}/api/v1/{path}')
    return f'https://{controller_ip}:{DNAC_port}/api/v1/{path}'

def get_url(url):
    url = create_url(path=url)
    #print(url)
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)
    
    return response.json()

def list_network_devices():
    #print(get_url("network-device"))
    return get_url("network-device")


if __name__ == "__main__":
    response = list_network_devices()
    print(f"[purple][bold]{'hostname':30}{'mgmt IP':17}{'serial':15}{'platformId':18}\
        {'SW Version':12}{'role':16}{'Uptime':15}[/bold][/purple]")

    for device in response['response']:
        uptime = "N/A" if device['upTime'] is None else device['upTime']

        print(f"{device['hostname']:30}{device['managementIpAddress']:17}{device['serialNumber']:15}{device['platformId']:18}\
        {device['softwareVersion']:12}{device['role']:16}{uptime:15}")

#if __name__ == "__main__":
#    get_auth_token()