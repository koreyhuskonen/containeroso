from uuid import uuid4

def getId():
    return uuid4().hex[:16]

def createDevice(deviceType="host"):
    device = {"id": getId()}
    device["type"] = deviceType
    if deviceType == "host":
        device["image"] = "virtuoso"
    device["connectedSwitches"] = []
    device["connectedRouters"] = []
    return device

def connect(d1, *args):
    for d2 in args:
        connectPair(d1, d2)
        connectPair(d2, d1)
        
def connectPair(d1, d2): 
    if d1["type"] == "switch":
        d2["connectedSwitches"].append(d1["id"])
    elif d1["type"] == "router":
        d2["connectedRouters"].append(d1["id"])

def makePayload(*args):
    return {"networkId": getId(), "machines": list(args)}

def makeNet(d):
    return {m[0]["id"]: [h["id"] for h in m[1]] for m in d}

def makeR(r):
    return [[d["id"] for d in g] for g in r]

#           S
#          / \
#         H   H 
s1 = createDevice("switch")
h1 = createDevice()
h2 = createDevice()
connect(s1, h1, h2)
p1 = makePayload(s1, h1, h2)
p1_net = {s1["id"]: [h1["id"], h2["id"]]}
p1_r = []
        
#           R
#          / \
#         S   S 
#         |   |
#         H   H
r1 = createDevice("router")
s1 = createDevice("switch")
s2 = createDevice("switch")
h1 = createDevice()
h2 = createDevice()
connect(r1, s1, s2)
connect(s1, h1)
connect(s2, h2)
p2 = makePayload(r1, s1, s2, h1, h2)
p2_net = {r1["id"]: [h1["id"], h2["id"]]}
p2_r = []

#         R - R
#         |   |
#         S   S 
#         |   |
#         H   H
r1 = createDevice("router")
r2 = createDevice("router")
s1 = createDevice("switch")
s2 = createDevice("switch")
h1 = createDevice()
h2 = createDevice()
connect(r1, r2, s1)
connect(r2, r1, s2)
connect(s1, h1)
connect(s2, h2)
p3 = makePayload(r1, r2, s1, s2, h1, h2)
net = ((r1, [h1]), (r2, [h2]))
p3_net = makeNet(net)
r = [(r1, r2)]
p3_r = makeR(r)
