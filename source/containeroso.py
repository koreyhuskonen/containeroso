#!/usr/local/bin/python3

from logger import info
from ipaddress import ip_network
import docker
client = docker.from_env()

subnetGen = ip_network('124.0.0.0/8').subnets(new_prefix=24)

def getIPAM():
    sub  = next(subnetGen)
    gate = next(sub.hosts())
    pool = docker.types.IPAMPool(subnet=str(sub), gateway=str(gate))
    ipam_config = docker.types.IPAMConfig(pool_configs=[pool])
    return ipam_config

def startContaineroso():
    info(f'Building image "virtuoso" if it does not already exist')
    client.images.build(path=".", dockerfile="Dockerfile.virtuoso", tag="virtuoso", rm=True)

def makeId(networkId, machineId):
    return networkId + '_' + machineId

def createNetwork(n):
    networkId = n["networkId"]
    info(f'Creating network {networkId}')

    machines = n["machines"]
    info('Creating machines')

    for m in machines:
        if m["type"] == 'router' or m["type"] == 'switch':
            machineId = makeId(networkId, m["id"])
            info(f'  {m["type"]} {machineId}')
            client.networks.create(machineId, 
                                   ipam=getIPAM())

    for m in machines:
        if m["type"] == 'host': 
            machineId = makeId(networkId, m["id"])
            info(f'  host {machineId}')
            client.containers.run(m["image"],
                                  name=machineId,
                                  detach=True,
                                  auto_remove=True,
                                  ports={'22/tcp': None})
            
            switches = m["connectedSwitches"]
            routers  = m["connectedRouters"]

            if len(switches) == 0 and len(routers) == 0:
                continue

            for switchId in switches:
                client.networks.get(makeId(networkId, switchId)).connect(machineId)
            
            for routerId in routers:
                client.networks.get(makeId(networkId, routerId)).connect(machineId)

            # Disconnect from Docker default bridge
            client.networks.list(names="bridge")[0].disconnect(machineId)

    for m in machines:
        if m["type"] == 'switch':
            switchId = makeId(networkId, m["id"])
            switch   = client.networks.get(switchId)
            routers  = m["connectedRouters"]
            
            if len(routers) > 0:
                for routerId in routers:
                    for con in switch.containers:
                        client.networks.get(makeId(networkId, routerId)).connect(con)

                for con in switch.containers:
                    switch.disconnect(con)

def destroyNetwork(networkId):
    info('Removing containers')
    for c in client.containers.list(filters={"name": networkId}):
        info(f'  {c.name}')
        c.remove(force=True)

    info(f'Removing networks')
    for n in client.networks.list(names=networkId):
        info(f'  {n.name}')
        n.remove()

def getSSHPort(machineId):
    ports = client.containers.get(machineId).ports
    hostPort = ports['22/tcp'][0]['HostPort']
    info(f'Machine {machineId} listening on port {hostPort}')
    return hostPort
