#!/usr/local/bin/python3

import docker
import paramiko
from itertools import combinations
from containeroso import createNetwork, destroyNetwork, getConnectedSwitches
from containeroso import getSSHPort, startContaineroso
from collections import defaultdict
from logger import info
from test_payload import *

cli = docker.from_env()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def testNetwork(p):
    startContaineroso()
    createNetwork(p)
    testConnections(p)
    #destroyNetwork(p["networkId"])

def testConnections(p):
    networkId = p["networkId"]

    hosts    = [m for m in p["machines"] if m["type"] == 'host']
    switches = [m for m in p["machines"] if m["type"] == 'switch']
    routers  = [m for m in p["machines"] if m["type"] == 'router']
    switchesConnectedToRouters = set()
    
    # Test remote access to each host
    for host in hosts:
        port = getSSHPort(host["id"])
        testSSH(port)
        info(f'ssh -> {host["id"]} ({port}) OK')
    
    for router in routers:
        routerId = router["id"]
        info(f'Testing hosts on router {routerId}')
        hostsConnectedToThisRouter = set()
        for host in hosts:
            if routerId in host["connectedRouters"]:
                hostsConnectedToThisRouter.add(host["id"])
        for switchId in router["connectedSwitches"]:
            switchesConnectedToThisSwitch = getConnectedSwitches(switches, switchId)
            switchesConnectedToRouters |= set(switchesConnectedToThisSwitch)
            for switchId in switchesConnectedToThisSwitch:
                for host in hosts:
                    if switchId in host["connectedSwitches"]:
                        hostsConnectedToThisRouter.add(host["id"])

        testHostConnections(routerId, hostsConnectedToThisRouter)

    for switch in switches:
        switchId = switch["id"]
        if switchId not in switchesConnectedToRouters:
            info(f'Testing hosts on switch {switchId}')
            hostsConnectedToThisSwitch = [host["id"] for host in hosts \
                                            if switchId in host["connectedSwitches"]]

            testHostConnections(switchId, hostsConnectedToThisSwitch)


def testHostConnections(dockerNetworkId, hosts):
    for pair in combinations(hosts, 2):
        testPairConnection(dockerNetworkId, *pair)
    
def testPairConnection(dockerNetworkId, id1, id2):
    nslookup(id1, id2)
    ping(dockerNetworkId, id1, id2)

def nslookup(id1, id2):
    con = cli.containers.get(id1)
    assert con.exec_run(f'nslookup {id2}').exit_code == 0
    info(f'  nslookup {id1} -> {id2} OK')
   
def ping(dockerNetworkId, id1, id2):
    con = cli.containers.get(id1)
    con2 = cli.containers.get(id2)
    ip = con2.attrs["NetworkSettings"]["Networks"][dockerNetworkId]["IPAddress"]
    assert con.exec_run(f'ping -c1 {ip}').exit_code == 0
    info(f'  ping {id1} -> {id2} ({ip}) OK')

def testSSH(port):
    ssh.connect('localhost', port=port, username='virtuoso', password='password')        
    ssh.close()

def clean():
    for c in cli.containers.list(all=True):
        c.remove(force=True)
    #cli.images.prune(filters={"dangling": False})
    cli.networks.prune()

if __name__ == '__main__':
    clean()
    testNetwork(test_payload1)
