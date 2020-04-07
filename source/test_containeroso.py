#!/usr/local/bin/python3

from containeroso import createNetwork, destroyNetwork
from containeroso import getSSHPort, startContaineroso, makeId
from uuid import uuid4

def uuid():
    return uuid4().hex

switch1Id = uuid()
switch2Id = uuid()
router1Id = uuid()
sample_payload1 = {
    "networkId": uuid(),
    "machines": [
        {
            "id": uuid(),
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                switch1Id
            ],
            "connectedRouters": []
        },
        {
            "id": uuid(),
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                switch2Id
            ],
            "connectedRouters": []
        },
        {
            "id": switch1Id,
            "type": "switch",
            "connectedSwitches": [],
            "connectedRouters": [
                router1Id
            ]
        },
        {
            "id": switch2Id,
            "type": "switch",
            "connectedSwitches": [],
            "connectedRouters": [
                router1Id
            ]
        },
        {
            "id": router1Id,
            "type": "router",
            "connectedSwitches": [],
            "connectedRouters": []
        }
    ]
}

def test(payload):
    startContaineroso()
    createNetwork(payload)
    networkId = payload["networkId"]
    getSSHPort(makeId(networkId, payload["machines"][0]["id"]))
    #destroyNetwork(networkId)


if __name__ == '__main__':
    test(sample_payload1)
