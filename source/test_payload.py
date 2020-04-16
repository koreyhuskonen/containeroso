p1 = {
    "networkId": "7f67800b1ba54e43a30e05819c4e4eef",
    "machines": [
        {
            "id": "03ae39b630544c23bfeb561306936fd0",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "2dc9f0d22abf4336b8ea3afff3f1e9f3"
            ],  
            "connectedRouters": []
        },  
        {   
            "id": "2dc9f0d22abf4336b8ea3afff3f1e9f3",
            "type": "switch",
            "connectedSwitches": [
               "2b80a00325f9402cba1baaf595bf49cd" 
            ], 
            "connectedRouters": []   
        },  
        {
            "id": "39c969f69b5149f9ad34415ab24e5924",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "2b80a00325f9402cba1baaf595bf49cd"
            ],  
            "connectedRouters": []
        },  
        {   
            "id": "2b80a00325f9402cba1baaf595bf49cd",
            "type": "switch",
            "connectedSwitches": [
                "2dc9f0d22abf4336b8ea3afff3f1e9f3"
            ], 
            "connectedRouters": [
                "060f741fdb2d4f198818d91c8adc4d08"
            ]   
        },  
        {   
            "id": "fa3bab03f56f4129847ec91dc159f8ca",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "6e2cf29a839b483cbd7ef5e0381c2e51"
            ],  
            "connectedRouters": []
        },  
        {   
            "id": "6e2cf29a839b483cbd7ef5e0381c2e51",
            "type": "switch",
            "connectedSwitches": [], 
            "connectedRouters": [
                "060f741fdb2d4f198818d91c8adc4d08"
            ]   
        },
        {
            "id": "060f741fdb2d4f198818d91c8adc4d08",
            "type": "router",
            "connectedSwitches": [
                "2b80a00325f9402cba1baaf595bf49cd",
                "6e2cf29a839b483cbd7ef5e0381c2e51"
            ],
            "connectedRouters": []
        },
        {
            "id": "ac7c298c5b66470ba0a0176dad6dfa0d",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [],  
            "connectedRouters": [
                "060f741fdb2d4f198818d91c8adc4d08" 
            ]
        },  
        {
            "id": "16bd4b7040dc44ee8d78fce264f31942",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [],  
            "connectedRouters": [
                "060f741fdb2d4f198818d91c8adc4d08" 
            ]
        }
    ]
}

#           S
#          / \
#         H   H 
p2 = {
    "networkId": "315086245b044416",
    "machines": [
        {   
            "id": "066855bf97b344d3",
            "type": "switch",
            "connectedSwitches": [], 
            "connectedRouters": []   
        },  
        {
            "id": "65b9fc408ef941cf",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "066855bf97b344d3"
            ],  
            "connectedRouters": []
        },  
        {
            "id": "646c4a0b3a264b09",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "066855bf97b344d3"
            ],  
            "connectedRouters": []
        }
    ]
}
p2_networks = {"066855bf97b344d3": ["65b9fc408ef941cf", "646c4a0b3a264b09"]}

#           R
#          / \
#         S   S 
#         |   |
#         H   H
p3 = {
    "networkId": "315086245b044416",
    "machines": [
        {   
            "id": "57f02616797a4c3c",
            "type": "router",
            "connectedSwitches": [
                "7196985f7abc4d8d",
                "2853e785eb974410"
            ], 
            "connectedRouters": []   
        },  
        {
            "id": "7196985f7abc4d8d",
            "type": "switch",
            "connectedSwitches": [],  
            "connectedRouters": [
                "57f02616797a4c3c"
            ]
        },  
        {
            "id": "e8a63f7c0cc1497a",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "7196985f7abc4d8d"
            ],  
            "connectedRouters": []
        },
        {
            "id": "2853e785eb974410",
            "type": "switch",
            "image": "virtuoso",
            "connectedSwitches": [],  
            "connectedRouters": [
                "57f02616797a4c3c"
            ]
        },
        {
            "id": "84743737379a4e24",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "2853e785eb974410"
            ],  
            "connectedRouters": []
        }
    ]
}
p3_networks = {"57f02616797a4c3c": ["e8a63f7c0cc1497a", "84743737379a4e24"]}

#         R - R
#         |   |
#         S   S 
#         |   |
#         H   H
p4 = {
    "networkId": "9dff566ee6d241cd",
    "machines": [
        {   
            "id": "c289065c3acb4382",
            "type": "router",
            "connectedSwitches": [
                "4a6836f269044525"
            ], 
            "connectedRouters": [
                "88e713c0a5fc4857"
            ]   
        },  
        {   
            "id": "88e713c0a5fc4857",
            "type": "router",
            "connectedSwitches": [
                "3f851fcbc60d40e5"
            ], 
            "connectedRouters": [
                "c289065c3acb4382"
            ]   
        },  
        {
            "id": "4a6836f269044525",
            "type": "switch",
            "connectedSwitches": [],  
            "connectedRouters": [
               "c289065c3acb4382" 
            ]
        },  
        {
            "id": "3f851fcbc60d40e5",
            "type": "switch",
            "connectedSwitches": [],  
            "connectedRouters": [
               "88e713c0a5fc4857" 
            ]
        },  
        {
            "id": "2d2c35f3970b4908",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "4a6836f269044525"
            ],  
            "connectedRouters": []
        },
        {
            "id": "330792492c994abc",
            "type": "host",
            "image": "virtuoso",
            "connectedSwitches": [
                "3f851fcbc60d40e5"
            ],  
            "connectedRouters": []
        }
    ]
}
p4_networks = {"c289065c3acb4382": ["2d2c35f3970b4908"],
               "88e713c0a5fc4857": ["330792492c994abc"]}
p4_routers = [("c289065c3acb4382", "88e713c0a5fc4857")]
