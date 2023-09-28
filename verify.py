import sys

def loadGraph(filename):
    file = open(filename, "r")
    edges = list()
    nodes = list()
    refillRooms = list()
    for line in file.readlines():
        parts = list(line.split(" "))
        lid = parts[0]
        if (lid == "node"):
            parts = line[6:-2].replace(",","").split(" ")
            nodes.append((int(parts[0]), float(parts[1]), float(parts[2])))
        if (lid == "e"):
            edges.append((int(parts[1]), int(parts[2])))
        if (lid == "source-node"):
            refillRooms.append(int(parts[1]))

    return {"nodes":nodes, "edges":edges, "refillRooms":refillRooms}

# Load plan
def loadPlan(filename):
    file = open(filename, "r")
    plan = list()
    for line in file.readlines():
        parts = list(line.strip().split(" "))
        plan.append(parts)
    return plan

def wrong(message, action):
    print("INCORRECT PLAN: could not execute action " + str(action))
    print("REASON: " + message)
    exit()

def checkPlan(plan, G):
    state = {"pos":0, "c1": -1, "c2":-1, "cols":dict()}
    edges = G["edges"]
    for action in plan:
        state = dict(state)
        state["cols"] = dict(state["cols"])
        if (action[0] == "MOVE"):
            op = int(action[2][4:])
            np = int(action[3][4:])
            if (op, np) not in edges and (np, op) not in edges:
                wrong("Start and goal vertex not connected.", action)
            if (state["pos"] != op):
                wrong("Painter not at the start position of the move.", action)
            if (np in state["cols"]):
                wrong("Goal vertex already painted.", action)
            state["pos"] = np
        if (action[0] == "FILLCONTAINER"):
            pos = int(action[2][4:])
            if (pos != state["pos"]):
                wrong("Painter not at refill location", action)
            if (pos not in G["refillRooms"]):
                wrong("Location not a refill location", action)
            if (action[3] not in {"CONTAINER0", "CONTAINER1"}):
                wrong("Invalid container argument.", action)
            if (action[4][5:] not in {"0", "1", "2", "3"}):
                wrong("Invalid color argument.", action)
            if action[3] == "CONTAINER0":
                state["c1"] = int(action[4][5:])
            else:
                state["c2"] = int(action[4][5:])
        if (action[0] == "PAINT"):
            pos = int(action[2][4:])
            color = int(action[3][5:])
            if (pos != state["pos"]):
                wrong("Painter not at paint location", action)
            if (color not in {0, 1, 2, 3}):
                wrong("Invalid color argument.", action)
            if action[4] == "CONTAINER0":
                if (state["c1"] != color):
                    wrong("Container does not containt the specified color", action)
                state["c1"] = -1
            else:
                if (state["c2"] != color):
                    wrong("Container does not containt the specified color", action)
                state["c2"] = -1
            state["cols"][state["pos"]] = color

if len(sys.argv) < 2:
    print("Usage: verify.py <problem-file> <plan-file>")
    exit()

problemFile = sys.argv[1]
planFile = sys.argv[2]
G = loadGraph(problemFile)
plan = loadPlan(planFile)
states = checkPlan(plan, G)
