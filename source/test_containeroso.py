#!/usr/local/bin/python3

import docker
import paramiko
from itertools import permutations

from containeroso import *
from logger import info
from test_payload import *

client = docker.from_env()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def testPayload(p, networks, connectedRouterGroups):
    networkId = p["networkId"]
    buildImage()
    createNetwork(p)
    info(f'Testing network {networkId}')
    # Test whether we created the correct number of Docker networks
    testNumNetworks(networks, networkId)
    # Test remote access
    testSSH(p)
    # Test network host connections
    testHostConnections(networks, connectedRouterGroups)
    # Destroy network
    destroyNetwork(networkId)

def testNumNetworks(networks, networkId):
    numNetworksCreated = len(client.networks.list(filters={"label": networkId}))
    assert numNetworksCreated == len(networks) 
    info(f"  Docker networks: {numNetworksCreated} OK")

def testHostConnections(networks, connectedRouterGroups):
    # Test connections between hosts on the same router
    for networkName, hosts in networks.items():
        info(f"  Hosts on {networkName}")
        for (id1, id2) in permutations(hosts, 2):
            testPair(networkName, id1, id2)

    # Test connections between hosts on different routers 
    for connectedRouters in connectedRouterGroups:
        info(f"  Hosts in router group: {connectedRouters}")
        for routerId in connectedRouters:
            for connectedRouterId in connectedRouters:
                if routerId != connectedRouterId:
                    for id1 in networks[routerId]:
                        for id2 in networks[connectedRouterId]:
                            testPair(connectedRouterId, id1, id2)

    
def testPair(networkName, id1, id2):
    #assert con1.exec_run(f'nslookup {id2}').exit_code == 0
    #info(f'    nslookup {id1} -> {id2} OK')
    con1 = client.containers.get(id1)
    con2 = client.containers.get(id2)

    ip = con2.attrs["NetworkSettings"]["Networks"][networkName]["IPAddress"]
    assert con1.exec_run(f'ping -c1 {ip}').exit_code == 0
    info(f'    ping {id1} -> {id2} ({ip}) OK')

def testSSH(p):
    for machine in p["machines"]:
        if machine["type"] == "host":
            port = getSSHPort(machine["id"])
            ssh.connect('localhost', port=port, username='virtuoso', password='password')
            ssh.close()
            info(f'    ssh -> {machine["id"]} OK')

def clean():
    for c in client.containers.list(all=True):
        c.remove(force=True)
    #client.images.prune(filters={"dangling": False})
    client.networks.prune()

if __name__ == '__main__':
    clean()
    for i in range(5, 7):
        p = eval(f"p{i}")
        p_net = eval(f"p{i}_net")
        p_r = eval(f"p{i}_r")
        testPayload(p, p_net, p_r)
