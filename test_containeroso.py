#!/usr/local/bin/python3

from containeroso import createNetwork, destroyNetwork, getSSHPort

sample_payload = {
    "networkId": "123",
    "machines": [
        {
            "id": "abc",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "sdf"
            ],
            "connectedRouters": []
        },
        {
            "id": "xyz",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "jkl"
            ],
            "connectedRouters": []
        },
        {
            "id": "sdf",
            "type": "switch",
            "connectedSwitches": [],
            "connectedRouters": [
                "vbn"
            ]
        },
        {
            "id": "jkl",
            "type": "switch",
            "connectedSwitches": [],
            "connectedRouters": [
                "vbn"
            ]
        },
        {
            "id": "vbn",
            "type": "router",
            "connectedSwitches": [],
            "connectedRouters": []
        }
    ]
}


createNetwork(sample_payload)
port = getSSHPort('123-abc')
print(f'Machine "123-abc" (networkId-machineId) port 22 is mapped to port {port} on the Docker host')
destroyNetwork('123')
