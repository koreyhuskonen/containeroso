#!/usr/local/bin/python3

from logger import info
from ipaddress import ip_network
import docker
client = docker.from_env()
cli = docker.APIClient()

subnets = ip_network('124.0.0.0/8').subnets(new_prefix=24)

def startContaineroso():
    info(f'Building image "virtuoso" if it does not already exist')
    client.images.build(path=".", dockerfile="Dockerfile.virtuoso", tag="virtuoso", rm=True)

def makeId(networkId, machineId):
    return networkId + '_' + machineId

def getIPAM():
    sub = next(subnets)
    gate = next(sub.hosts())
    pool = docker.types.IPAMPool(subnet=str(sub), gateway=str(gate))
    ipam_config = docker.types.IPAMConfig(pool_configs=[pool])
    return ipam_config

def createNetwork(n):
    networkId = n["networkId"]
    info(f'Creating network {networkId}')

    machines = n["machines"]
    info('Creating machines')

    for m in machines:
        if m["type"] == 'router' or m["type"] == 'switch':
            machineId = makeId(networkId, m["id"])
            info(f'  {m["type"]} {machineId}')
            client.networks.create(machineId, ipam=getIPAM())

    for m in machines:
        if m["type"] == 'host': 
            machineId = makeId(networkId, m["id"])
            info(f'  host {machineId}')
            cli.create_container(
                m["image"], 
                name=machineId,
                ports=[22],
                host_config=cli.create_host_config(port_bindings={22: None})
            )
            
            connected = m["connectedSwitches"] + m["connectedRouters"]

            if len(connected) == 0:
                continue

            for connectedId in connected:
                net = client.networks.get(makeId(networkId, connectedId))
                net.connect(machineId, aliases=[m["id"]])

            # Disconnect from Docker default bridge
            client.networks.list(names="bridge")[0].disconnect(machineId)

            # Start container
            cli.start(machineId)

    for m in machines:
        if m["type"] == 'switch':
            switchId = makeId(networkId, m["id"])
            switch = client.networks.get(switchId)
            routers = m["connectedRouters"]
            
            if len(routers) > 0:
                for routerId in routers:
                    for con in switch.containers:
                        net = client.networks.get(makeId(networkId, routerId))
                        net.connect(con, aliases=[con.name.split('_')[1]])

                for con in switch.containers:
                    switch.disconnect(con)

    for m in machines:
        if m["type"] == 'host':
            cli.restart(makeId(networkId, m["id"]))
            
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
