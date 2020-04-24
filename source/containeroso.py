#!/usr/local/bin/python3

from collections import deque
from logger import info
from ipaddress import ip_network
import docker
client = docker.from_env()

def buildImage(name="virtuoso"):
    info(f'Building image {name}')
    client.images.build(path=".", dockerfile="Dockerfile.virtuoso", tag=name, rm=True)

def createNetwork(n):
    networkId = n["networkId"]
    info(f'Creating network {networkId}')
    
    hosts    = [m for m in n["machines"] if m["type"] == 'host']
    switches = [m for m in n["machines"] if m["type"] == 'switch']
    routers  = [m for m in n["machines"] if m["type"] == 'router']
    HostToRouter = dict() #hostDefaultGatewayLookup
    visitedSwitches = set()
    
    for host in hosts:
        createVirtualHost(networkId, host)

    for router in routers:
        createVirtualNetwork(networkId, router["id"])
        createVirtualGateway(networkId, router["id"])

    for router in routers:
        configureGateway(router["id"], routers)

    for router in routers:
        routerId = router["id"]
        info(f'  router {routerId}')
        hostsConnectedToRouter, switchesConnectedToRouter = getHostsConnectedToRouter(hosts, switches+routers, routerId)
        visitedSwitches |= set(switchesConnectedToRouter)
        for hostId in hostsConnectedToRouter:
            if hostId in HostToRouter:
                raise NetworkError(f"Host {hostId} is connected to more than 1 router")
            HostToRouter[hostId] = routerId

        connectHostsToDevice(hostsConnectedToRouter, routerId)

    for switch in switches:
        switchId = switch["id"]
        if switchId not in visitedSwitches:
            info(f'  switch {switchId}')
            hostsConnectedToSwitch, switchesConnectedToSwitch = getHostsConnectedToSwitch(hosts, switches, switchId)
            visitedSwitches |= set(switchesConnectedToSwitch)
            createVirtualNetwork(networkId, switchId)
            connectHostsToDevice(hostsConnectedToSwitch, switchId)

    restartHostsAndSetDefaultGateway(hosts, HostToRouter)

def restartHostsAndSetDefaultGateway(hosts, HostToRouter):
    for host in hosts:
        hostId = host["id"]
        con = client.containers.get(hostId)
        con.restart()
        if hostId in HostToRouter:
            routerId = HostToRouter[hostId]
            gateway = client.containers.get(routerId)
            networks = gateway.attrs["NetworkSettings"]["Networks"]
            gatewayAddr = networks[routerId]["IPAddress"]
            for networkId in networks:
                if networkId != routerId:
                    net = client.networks.get(networkId)
                    subnet = net.attrs["IPAM"]["Config"][0]["Subnet"]
                    con.exec_run(f"ip route add {subnet} via {gatewayAddr}")

def connectHostsToDevice(hostIds, deviceId):
    net = client.networks.get(deviceId)
    for hostId in hostIds:
        info(f'    connect {hostId}')
        net.connect(hostId, aliases=[hostId])

def getHostsConnectedToRouter(hosts, switches, routerId):
    hostsConnectedToRouter, switchesConnectedToRouter = getHostsConnectedToSwitch(hosts, switches, routerId)
    hostsConnectedToRouter |= getHostsDirectlyConnectedTo(hosts, routerId, "Routers")
    return hostsConnectedToRouter, switchesConnectedToRouter[1:]

def getHostsDirectlyConnectedTo(hosts, deviceId, deviceType):
    hostsDirectlyConnected = set()
    for host in hosts:
        if deviceId in host[f"connected{deviceType}"]:
            hostsDirectlyConnected.add(host["id"])
    return hostsDirectlyConnected

def getHostsConnectedToSwitch(hosts, switches, switchId):
    hostsConnectedToSwitch = set()
    switchesConnectedToSwitch = getConnectedDevices(switches, switchId, "Switches")
    for connectedSwitchId in switchesConnectedToSwitch:
        hostsConnectedToSwitch |= getHostsDirectlyConnectedTo(hosts, connectedSwitchId, "Switches")
    return hostsConnectedToSwitch, switchesConnectedToSwitch

def createVirtualNetwork(networkId, deviceId):
    return client.networks.create(name=deviceId, 
                                  ipam=getIPAM(),
                                  labels={networkId: ""})

def createVirtualGateway(networkId, routerId):
    return client.containers.run(image="virtuoso",
                                 name=routerId,
                                 network=routerId,
                                 detach=True,
                                 privileged=True,
                                 labels={networkId: ""})

def configureGateway(routerId, routers):
    gateway = client.containers.get(routerId)
    gateway.exec_run("iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
    routersConnectedToThisRouter = getConnectedDevices(routers, routerId, "Routers")
    for i, connectedRouterId in enumerate(routersConnectedToThisRouter[1:], start=1):
        net = client.networks.get(connectedRouterId)
        net.connect(gateway)
        gateway.exec_run(f"iptables -A FORWARD -i eth{i} -o eth0 -j ACCEPT")
        gateway.exec_run(f"iptables -A FORWARD -i eth0 -o eth{i} -m state --state RELATED,ESTABLISHED -j ACCEPT")

def createVirtualHost(networkId, host):
    con = client.containers.run(image=host["image"],
                                name=host["id"],
                                detach=True,
                                privileged=True,
                                labels={networkId: ""},
                                ports={'22/tcp': None})
    
    if len(host["connectedSwitches"] + host["connectedRouters"]) > 0:
        # Disconnect from Docker default bridge
        client.networks.list(names="bridge")[0].disconnect(con)

subnet = ip_network('192.168.0.0/16').subnets(new_prefix=24)

def getIPAM():
    sub = next(subnet)
    gate = next(sub.hosts())
    pool = docker.types.IPAMPool(subnet=str(sub), gateway=str(gate)) 
    ipam_config = docker.types.IPAMConfig(pool_configs=[pool])
    return ipam_config

def getConnectedDevices(devices, srcId, deviceType):
    queue = deque([srcId])
    visited = []
    while(queue):
        deviceId = queue.popleft()
        if deviceId not in visited:
            visited.append(deviceId)
            for device in devices:
                if deviceId == device["id"]:
                    connectedDevices = device[f"connected{deviceType}"]
                    queue += deque(connectedDevices)

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
    return hostPort

class NetworkError(Exception):
    def __init__(self, message):
        self.message = message

