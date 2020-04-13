#!/usr/local/bin/python3

import docker
import paramiko
from itertools import combinations
from collections import defaultdict

from containeroso import *
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
    visitedSwitches = set()
    
    # Test remote access to each host
    for host in hosts:
        port = getSSHPort(host["id"])
        testSSH(port)
        info(f'ssh -> {host["id"]} ({port}) OK')
    
    for router in routers:
        routerId = router["id"]
        info(f'Testing hosts on router {routerId}')
        hostsConnectedToRouter, switchesConnectedToRouter = getHostsConnectedToRouter(hosts, switches, routerId)
        visitedSwitches |= set(switchesConnectedToRouter)
        testHostConnections(routerId, hostsConnectedToRouter)

    for switch in switches:
        switchId = switch["id"]
        if switchId not in visitedSwitches:
            info(f'Testing hosts on switch {switchId}')
            hostsConnectedToSwitch, switchesConnectedToSwitch = getHostsConnectedToSwitch(hosts, switches, switchId)
            visitedSwitches |= set(switchesConnectedToSwitch)
            testHostConnections(switchId, hostsConnectedToSwitch)

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
