#!/usr/local/bin/python3

from collections import deque
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
    
    hosts    = [m for m in machines if m["type"] == 'host']
    switches = [m for m in machines if m["type"] == 'switch']
    routers  = [m for m in machines if m["type"] == 'router']
    switchesConnectedToRouters = set()
    
    for host in hosts:
        hostId = makeId(networkId, host["id"])
        client.containers.create(image=host["image"],
                                 name=hostId,
                                 detach=True,
                                 ports={'22/tcp': None})

        if len(host["connectedSwitches"] + host["connectedRouters"]) > 0:
            client.networks.list(names="bridge")[0].disconnect(hostId)

    for router in routers:
        routerId = makeId(networkId, host["id"])
        net = client.networks.create(name=routerId, ipam=getIPAM())
        for host in hosts:
            if router["id"] in host["connectedRouters"]:
                net.connect(makeId(networkId, host["id"]), aliases=[host["id"]])
        for switch in switches:
            if router["id"] in switch["connectedRouters"]:
                switchesConnectedToThisRouter = getConnectedSwitches(switches, switch["id"])
                switchesConnectedToRouters |= set(switchesConnectedToThisRouter)
                for switchId in switchesConnectedToThisRouter:
                    for s in switches:
                        if s["id"] == switchId:
                            for host in hosts:
                                if s["id"] in host["connectedSwitches"]:
                                    net.connect(makeId(networkId, host["id"]), aliases=[host["id"]])

    for switch in switches:
        switchId = switch["id"]
        if switchId not in switchesConnectedToRouters:
            net = client.networks.create(name=switchId, ipam=getIPAM())
            for host in hosts:
                if switchId in host["connectedSwitches"]:
                    net.connect(makeId(networkId, host["id"]), aliases=[host["id"]])
            for connectedSwitch in switch["connectedSwitches"]:
                # TODO add link using pipework
                pass
     
    for host in hosts:
        cli.start(makeId(networkId, host["id"]))
           
def getConnectedSwitches(switches, src):
    queue = deque([src])
    visited = []
    while(queue):
        nextSwitch = queue.popleft()
        if nextSwitch not in visited:
            visited.append(nextSwitch)
            for switch in switches:
                if switch["id"] == nextSwitch:
                    connectedSwitches = switch["connectedSwitches"]
                    queue += deque(connectedSwitches)

    return visited
            
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
