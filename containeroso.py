#!/usr/local/bin/python3

from logger import info
import docker
client = docker.from_env()

def createNetwork(n):
    networkId = n["networkId"]
    machines  = n["machines"]

    info(f'Creating network {networkId}')
    net = client.networks.create(networkId)

    info('Creating machines...')
    for m in machines:
        if m["type"] != 'host': 
            continue

        machineId = networkId + '-' + m["id"]
        image     = m["image"]
        info(f'  {machineId}')
        client.containers.run(image, \
                name=machineId, \
                detach=True, \
                auto_remove=True, \
                publish_all_ports=True, \
                network=net.id)

def destroyNetwork(networkId):
    net = client.networks.get(networkId)

    info('Removing containers...')
    for c in net.containers:
        info(f'  {c.name}')
        c.remove(force=True)

    info(f'Removing network {net.name}')
    net.remove()

def getSSHPort(machineId):
    con = client.containers.get(machineId) 
    ports = con.ports
    return ports['22/tcp'][0]['HostPort']
