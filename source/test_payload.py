from uuid import uuid4

def uuid():
    return uuid4().hex

switch1Id = uuid()
switch2Id = uuid()
router1Id = uuid()
test_payload1 = {
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
            "connectedSwitches": [
                switch2Id
            ], 
            "connectedRouters": [
                router1Id
            ]   
        },  
        {   
            "id": switch2Id,
            "type": "switch",
            "connectedSwitches": [
                switch1Id
            ], 
            "connectedRouters": [
                router1Id
            ]   
        },
        {
            "id": router1Id,
            "type": "router",
            "connectedSwitches": [
                switch1Id,
                switch2Id
            ],
            "connectedRouters": []
        }
    ]
}
