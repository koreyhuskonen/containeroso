#!/usr/local/bin/python3

from containeroso import createNetwork, destroyNetwork
from containeroso import getSSHPort, startContaineroso

sample_payload1 = {
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

sample_payload2 = {
    "networkId": "567",
    "machines": [
        # This machine is not connected to anything
        {
            "id": "abc",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [],
            "connectedRouters": []
        },
        {
            "id": "nop",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "jkl"
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
            "id": "jkl",
            "type": "switch",
            "connectedSwitches": [],
            "connectedRouters": [
                "vbn"
            ]
        },
    ]
}


if __name__ == '__main__':
    startContaineroso()
    createNetwork(sample_payload1)
    getSSHPort('123-abc')
    destroyNetwork('123')

    createNetwork(sample_payload2)
    getSSHPort('567-xyz')
    destroyNetwork('567')
