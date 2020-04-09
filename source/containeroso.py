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
        info(f'  host {host["id"]}')
        client.containers.create(image=host["image"],
                                 name=host["id"],
                                 detach=True,
                                 labels={networkId: ""},
                                 ports={'22/tcp': None})

        if len(host["connectedSwitches"] + host["connectedRouters"]) > 0:
            # Disconnect from Docker default bridge
            client.networks.list(names="bridge")[0].disconnect(host["id"])

    for router in routers:
        info(f'  router {router["id"]}')
        hostsConnectedToThisRouter = set()
        for host in hosts:
            # Hosts directly connected to the router
            if router["id"] in host["connectedRouters"]:
                hostsConnectedToThisRouter.add(host["id"])
        for switchId in router["connectedSwitches"]:
            switchesConnectedToThisSwitch = getConnectedSwitches(switches, switchId)
            switchesConnectedToRouters |= set(switchesConnectedToThisSwitch)
            for switchId in switchesConnectedToThisSwitch:
                for host in hosts:
                    if switchId in host["connectedSwitches"]:
                        # Hosts connected to a switch with a path to the router
                        hostsConnectedToThisRouter.add(host["id"])
        
        net = client.networks.create(name=router["id"], 
                                     ipam=getIPAM(),
                                     labels={networkId: ""})
        for hostId in hostsConnectedToThisRouter:
            info(f'    connect {hostId}') 
            net.connect(hostId, aliases=[hostId])

        for routerId in router["connectedRouters"]:
            # TODO add links between routers
            pass

    for switch in switches:
        switchId = switch["id"]
        if switchId not in switchesConnectedToRouters:
            info(f'  switch {switchId}')
            net = client.networks.create(name=switchId, 
                                         ipam=getIPAM(),
                                         labels={networkId: ""})
            for host in hosts:
                if switchId in host["connectedSwitches"]:
                    info(f'    connect {host["id"]}') 
                    net.connect(host["id"], aliases=[host["id"]])
            for connectedSwitch in switch["connectedSwitches"]:
                # TODO add links between switches
                pass
     
    for host in hosts:
        cli.start(host["id"])
           
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
    for c in client.containers.list(filters={"label": networkId}):
        info(f'  {c.name}')
        c.remove(force=True)

    info(f'Removing networks')
    for n in client.networks.list(filters={"label": networkId}):
        info(f'  {n.name}')
        n.remove()

def getSSHPort(machineId):
    ports = client.containers.get(machineId).ports
    hostPort = ports['22/tcp'][0]['HostPort']
    info(f'Machine {machineId} listening on port {hostPort}')
    return hostPort
