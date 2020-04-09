#!/usr/local/bin/python3

import docker
import paramiko
from itertools import combinations
from containeroso import createNetwork, destroyNetwork
from containeroso import getSSHPort, startContaineroso, makeId
from collections import defaultdict
from logger import info
from test_payload import *

cli = docker.from_env()
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def testSSH(port):
    client.connect('localhost', port=port, 
                    username='virtuoso', password='password')        
    client.close()

def testNetwork(p):
    startContaineroso()
    createNetwork(p)

    networkId = p["networkId"]
    hosts = [m for m in p["machines"] if m["type"] == 'host']
    switches = [m for m in p["machines"] if m["type"] == 'switch']
    networkGroups = defaultdict(set)

    for host in hosts:
        hostId = host["id"]
        port = getSSHPort(makeId(networkId, hostId))
        testSSH(port)
        info(f'ssh -> {hostId} ({port}) OK')
        
        for cId in host["connectedSwitches"] + host["connectedRouters"]:
            networkGroups[cId].add(hostId)
            
    for switch in switches:
        switchId = switch["id"]
        for cSwitchId in switch["connectedSwitches"]:
            networkGroups[switchId] |= networkGroups[cSwitchId]
    
    for switch in switches:
        switchId = switch["id"]
        for routerId in switch["connectedRouters"]:
            networkGroups[routerId] |= networkGroups[switchId]
    
    connectedPairs = set()
    for switchOrRouter, connectedHosts in networkGroups.items():
        for pair in combinations(connectedHosts, 2):
            connectedPairs.add(pair)
    
    for pair in connectedPairs:
        testPairConnection(networkId, *pair)

    print(networkGroups)
    print(connectedPairs) 
    #destroyNetwork(networkId)

def testPairConnection(networkId, id1, id2):
    nslookup(networkId, id1, id2)
    nslookup(networkId, id2, id1)
    ping(networkId, id1, id2)
    ping(networkId, id2, id1)

def nslookup(networkId, id1, id2):
    info(f'nslookup {id1} -> {id2}')
    con = cli.containers.get(makeId(networkId, id1))
    assert con.exec_run(f'nslookup {id2}').exit_code == 0
   
def ping(networkId, id1, id2):
    info(f'ping {id1} -> {id2}')
    con = cli.containers.get(makeId(networkId, id1))
    assert con.exec_run(f'ping -c1 {id2}').exit_code == 0
    

def clean():
    for c in cli.containers.list(all=True):
        c.remove(force=True)
    #cli.images.prune(filters={"dangling": False})
    cli.networks.prune()

if __name__ == '__main__':
    clean()
    testNetwork(test_payload1)
