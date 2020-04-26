[![Build Status](https://travis-ci.org/koreyhuskonen/containeroso.svg?branch=master)](https://travis-ci.org/koreyhuskonen/containeroso)
[![License: MIT](https://img.shields.io/badge/License-MIT-blueviolet.svg)](https://opensource.org/licenses/MIT)

# Containeroso 
Containeroso is a Virtual Network Creation Engine (VNCE) that highly leverages Docker to emulate devices. With Containeroso, you can instantly spin up a lightweight virtual network according to a user-defined specification. Containeroso is meant to be used as a component of [Virtuoso](https://github.com/Samwisebuze/senior-design), a platform that allows you to create virtual networks simply by dragging and dropping devices onto a network diagram, all from a web browser. 
## How it works
Containeroso allows you to **declaratively** build virtual networks. You describe the machines you want in the network and how they're connected, and Containeroso does the rest. Currently, Containeroso only supports networks that consist of hosts, switches, and routers. To emulate hosts, Containeroso uses custom Docker containers outfitted with standard networking tools. To emulate switches and routers, Containeroso uses a combination of Docker networks and containers which function as default gateways with pre-configured iptables. No host can be connected to more than 1 router. See the `Examples` section for details.
## Try it out
To build:
```
docker build -t containeroso .
```
To run:
```
docker run -t -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock containeroso
```
## API Documentation
**Route**|**Method**|**Data**|**Description**
:-----|:-----:|:-----:|:-----:
/api/create-network|POST|See examples|Create a virtual network
/api/delete-network|DELETE|{"networkId": "123-456-789-xyz"}|Delete a virtual network
/api/get-port|POST|{"machineId": "456-abc-rty-789"}|Get the port you need to SSH into the machine
/api/status|GET| |Check whether the server is running
## Examples
### Network 1
```
           R
          / \
         S   S 
         |   |
         H   H
```
To create the network:
```
curl --location --request POST 'localhost:5000/api/create-network' \
--header 'Content-Type: application/json' \
--data-raw '{
  "networkId": "c3c89a580b134328",
  "machines": [
    {
      "id": "660fd7b1403f4987",
      "type": "router",
      "connectedSwitches": [
        "94b23262766645ef",
        "c544e38077934351"
      ],
      "connectedRouters": []
    },
    {
      "id": "94b23262766645ef",
      "type": "switch",
      "connectedSwitches": [],
      "connectedRouters": [
        "660fd7b1403f4987"
      ]
    },
    {
      "id": "c544e38077934351",
      "type": "switch",
      "connectedSwitches": [],
      "connectedRouters": [
        "660fd7b1403f4987"
      ]
    },
    {
      "id": "f63be7d3d02f43f7",
      "type": "host",
      "image": "virtuoso",
      "connectedSwitches": [
        "94b23262766645ef"
      ],
      "connectedRouters": []
    },
    {
      "id": "2428c72d2a5e4be5",
      "type": "host",
      "image": "virtuoso",
      "connectedSwitches": [
        "c544e38077934351"
      ],
      "connectedRouters": []
    }
  ]
}'
```
To delete this network:
```
curl --location --request DELETE 'localhost:5000/api/delete-network' \
--header 'Content-Type: application/json' \
--data-raw '{
    "networkId": "c3c89a580b134328"
}'
```
### Network 2
```
         R - R
         |   |
         S   S 
         |   |
         H   H
```
To create the network:
```
curl --location --request POST 'localhost:5000/api/create-network' \
--header 'Content-Type: application/json' \
--data-raw '{
  "networkId": "2f8011e47f624f36",
  "machines": [
    {
      "id": "3513618bd817495f",
      "type": "router",
      "connectedSwitches": [
        "d90522cddb344fa7"
      ],
      "connectedRouters": [
        "402d45f421e24e6e"
      ]
    },
    {
      "id": "402d45f421e24e6e",
      "type": "router",
      "connectedSwitches": [
        "65390308c4064d6b"
      ],
      "connectedRouters": [
        "3513618bd817495f"
      ]
    },
    {
      "id": "d90522cddb344fa7",
      "type": "switch",
      "connectedSwitches": [],
      "connectedRouters": [
        "3513618bd817495f"
      ]
    },
    {
      "id": "65390308c4064d6b",
      "type": "switch",
      "connectedSwitches": [],
      "connectedRouters": [
        "402d45f421e24e6e"
      ]
    },
    {
      "id": "ba805339a7fd4893",
      "type": "host",
      "image": "virtuoso",
      "connectedSwitches": [
        "d90522cddb344fa7"
      ],
      "connectedRouters": []
    },
    {
      "id": "1ffebc91bf6c4ab3",
      "type": "host",
      "image": "virtuoso",
      "connectedSwitches": [
        "65390308c4064d6b"
      ],
      "connectedRouters": []
    }
  ]
}'
```
If you want to connect to host `1ffebc91bf6c4ab3` via SSH, you can find the port it's running on via:
```
curl --location --request POST 'localhost:5000/api/get-port' \
--header 'Content-Type: application/json' \
--data-raw '{
    "machineId": "1ffebc91bf6c4ab3"
}'
```
