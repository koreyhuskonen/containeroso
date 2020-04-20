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
net = [(s1, [h1, h2])]
p1_net = makeNet(net)
p1_r = []

#           R
#          / \
#         H   H 
r1 = createDevice("router")
h1 = createDevice()
h2 = createDevice()
connect(r1, h1, h2)
p2 = makePayload(r1, h1, h2)
net = [(r1, [h1, h2])]
p2_net = makeNet(net)
p2_r = []
        
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
connect(s1, r1, h1)
connect(s2, r1, h2)
p3 = makePayload(r1, s1, s2, h1, h2)
net = [(r1, [h1, h2])]
p3_net = makeNet(net)
p3_r = []

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
connect(s1, r1, h1)
connect(s2, r2, h2)
p4 = makePayload(r1, r2, s1, s2, h1, h2)
net = [(r1, [h1]), (r2, [h2])]
p4_net = makeNet(net)
r = [(r1, r2)]
p4_r = makeR(r)

#     R - R - R - R
#     |   |   |   | 
#     H   S   S   H
#         |   |  
#         H   H
r1 = createDevice("router")
r2 = createDevice("router")
r3 = createDevice("router")
r4 = createDevice("router")
s1 = createDevice("switch")
s2 = createDevice("switch")
h1 = createDevice()
h2 = createDevice()
h3 = createDevice()
h4 = createDevice()
connect(r1, r2, h1)
connect(r2, r1, r3, s1)
connect(r3, r2, r4, s2)
connect(r4, r3, h4)
connect(s1, r2, h2)
connect(s2, r3, h3)
p5 = makePayload(r1, r2, r3, r4, s1, s2, h1, h2, h3, h4)
net = [(r1, [h1]), (r2, [h2]), (r3, [h3]), (r4, [h4])]
p5_net = makeNet(net)
r = [(r1, r2, r3, r4)]
p5_r = makeR(r)

#     H - S - S - H
#         |   |
#         H   H 
s1 = createDevice("switch")
s2 = createDevice("switch")
h1 = createDevice()
h2 = createDevice()
h3 = createDevice()
h4 = createDevice()
connect(s1, s2, h1, h2) 
connect(s2, s1, h3, h4)
p6 = makePayload(s1, s2, h1, h2, h3, h4)
net = [(s1, [h1, h2, h3, h4])]
p6_net = makeNet(net)
p6_r = []

#     H - S - S - R
#         |   
#         H   
r1 = createDevice("router")
s1 = createDevice("switch")
s2 = createDevice("switch")
h1 = createDevice()
h2 = createDevice()
connect(s1, s2, h1, h2)
connect(s2, s1, r1)
connect(r1, s2)
p7 = makePayload(r1, s1, s2, h1, h2)
net = [(r1, [h1, h2])]
p7_net = makeNet(net)
p7_r = []

#         R
#         |
#         S
#         |
#         H - S - H    
r1 = createDevice("router")
s1 = createDevice("switch")
s2 = createDevice("switch")
h1 = createDevice()
h2 = createDevice()
connect(r1, s1)
connect(s1, r1, h1)
connect(s2, h1, h2)
p8 = makePayload(r1, s1, s2, h1, h2)
net = [(r1, [h1]), (s2, [h1, h2])]
p8_net = makeNet(net)
p8_r = []

#         R
#         |
#         S   R
#         |   |
#         H - S  
r1 = createDevice("router")
r2 = createDevice("router")
s1 = createDevice("switch")
s2 = createDevice("switch")
h1 = createDevice()
connect(r1, s1)
connect(s1, r1, h1)
connect(s2, r2, h1)
connect(r2, s2)
p9 = makePayload(r1, r2, s1, s2, h1)
net = [(r1, [h1]), (r2, [h1])]
p9_net = makeNet(net)
p9_r = []
