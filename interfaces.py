from acitoolkit.acitoolkit import *
import credentials
import requests
import json

# Authentication
auth = requests.post(f'{credentials.url}/api/aaaLogin.json', json={'aaaUser':{"attributes":{'name':credentials.user,'pwd':credentials.psw}}}, verify=False)
auth_json = auth.json()
token = auth_json["imdata"][0]["aaaLogin"]["attributes"]["token"]
cookie = {'APIC-cookie': token}

def verify_node_port_pod():
    # Interactive: POD, Node, and Port ID
    pod_id = input("Enter the POD ID [1, 2, 3, etc]: ")
    node_id = input("Enter the Node ID [101, 102, 201, 202, etc]: ")
    port_id = input("Enter the Port ID [1/1, 1/2, 1/3, 1/4, etc]: ")

    # HTTP GET Request
    response = requests.get(f'{credentials.url}/api/node/mo/topology/pod-{pod_id}/node-{node_id}/sys/phys-[eth{port_id}]/dbgEtherStats.json', cookies=cookie, verify=False)

    # Verify Response Code
    if response.status_code == 200:
        # JSON Formatting
        data = response.json()

        # Retrieve data
        rmon_ether_stats = data['imdata'][0]['rmonEtherStats']['attributes']
        
        broadcast_pkts = rmon_ether_stats['broadcastPkts']
        multicast_pkts = rmon_ether_stats['multicastPkts']
        pkts = rmon_ether_stats['pkts']

        # Print Data
        print(f"broadcastPkts: {broadcast_pkts}")
        print(f"multicastPkts: {multicast_pkts}")
        print(f"pkts: {pkts}")
    else:
        print(f"HTTP Request error: {response.status_code}")

    another = input("Do you want to verify other Node/Port/POD IDs? (yes/no): ")
    if another.lower() == "yes":
        verify_node_port_pod()  # Recursively call the function if the user wants to verify more IDs

# Call the function to start the verification process
verify_node_port_pod()