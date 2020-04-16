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
