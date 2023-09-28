import pygame
import sys

def loadImg(name, scale):
    asstetsDir='assets/'
    img = pygame.image.load(asstetsDir + name + '.png')
    img = pygame.transform.scale_by(img, scale)
    return img

def drawText(screen, text, x, y, size=32):
    font = pygame.font.Font('freesansbold.ttf', size)
    textSurface = font.render(text, True, (0,0,0))
    screen.blit(textSurface, (x,y))
 
def drawPainter(screen, painterImg, nodes, index1, index2, progress):
    (w,h) = screen.get_size()
    (x1,y1) = nodes[index1][1:]
    (x2,y2) = nodes[index2][1:]
    (x,y) = (x1 + progress*(x2-x1), y1 + progress*(y2-y1))
    screen.blit(painterImg, (w*x - painterImg.get_width()/2, h*y-painterImg.get_height()))


def main():

    screenWidth = 1000
    screenHeigth = 800
    bgColor = (220, 240, 220)
     
    pygame.init()
    pygame.display.set_caption("Painter Demo")
     
    screen = pygame.display.set_mode((screenWidth,screenHeigth))
    running = True

    G = loadGraph(problemFile)
    plan = loadPlan(planFile)

    state = {"pos":0, "c1": -1, "c2":-1, "cols":dict()}
    states = planToStates(plan, state, G)

    painterImg = loadImg('painter', 0.5)
    refillImg = loadImg('refill', 0.15)
    bucketImg = dict()
    bucketImg['-1'] = loadImg('empty-bucket', 0.3)
    bucketImg['0'] = loadImg('yellow-bucket', 0.3)
    bucketImg['1'] = loadImg('green-bucket', 0.3)
    bucketImg['2'] = loadImg('blue-bucket', 0.3)
    bucketImg['3'] = loadImg('red-bucket', 0.3)
    

    nextStep = 0
    started = False

    stepTime = 500
    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == 27):
                    running = False
                    break
                if (event.key == 32):
                    started = True
                    lastStepAt = pygame.time.get_ticks()
                    break
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        if (started):
            now = pygame.time.get_ticks()
            stepProgress = (now - lastStepAt)/stepTime
            if (now - lastStepAt >= stepTime):
                nextStep += 1
                lastStepAt = now
                stepProgress = 0

        if (nextStep >= len(states)):
            drawText(screen, "Plan Simulation Finished", 300, 20)
            pygame.display.flip()
            continue

        state = states[nextStep]

        screen.fill(bgColor)
        screen.blit(bucketImg[str(state["c1"])], (screenWidth - 130, 0))
        screen.blit(bucketImg[str(state["c2"])], (screenWidth - 70, 0))
        if (nextStep < len(plan)):
            drawText(screen, str(plan[nextStep]), 20, 750, 22)

        if (not started):
            drawText(screen, "Press <space> to Start", 300, 20)
            stepProgress = 1

        #for edge in G.edges:
        #    edge[0].pos
        for e in G["edges"]:
            x1 = int(screenWidth * G["nodes"][e[0]][1])
            y1 = int(screenHeigth * G["nodes"][e[0]][2])
            x2 = int(screenWidth * G["nodes"][e[1]][1])
            y2 = int(screenHeigth * G["nodes"][e[1]][2])
            pygame.draw.aaline(screen, (0,0,0), (x1,y1), (x2, y2))
        nodes = G["nodes"]

        for r in G["refillRooms"]:
            screen.blit(refillImg, (screenWidth*nodes[r][1] - refillImg.get_width()/2,screenHeigth*nodes[r][2]-refillImg.get_height()))

        if (nextStep > 0):
            drawPainter(screen, painterImg, nodes, states[nextStep-1]["pos"], state["pos"], stepProgress)
        else:
            drawPainter(screen, painterImg, nodes, state["pos"], state["pos"], stepProgress)
        for n in nodes:
            pointColor = bgColor
            if (n[0] in state["cols"]):
                col = state["cols"][n[0]]
                if (col == 0):
                    pointColor = (255,255,0)
                if (col == 1):
                    pointColor = (0,255,0)
                if (col == 2):
                    pointColor = (0,0,255)
                if (col == 3):
                    pointColor = (255,0,0)
            pygame.draw.circle(screen, (0,0,0), (n[1]*screenWidth, n[2]*screenHeigth), 15, 0)
            pygame.draw.circle(screen, pointColor, (n[1]*screenWidth, n[2]*screenHeigth), 13, 0)
        pygame.display.flip()

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

def planToStates(plan, initialState, G):
    states = list()
    states.append(initialState)
    state = initialState
    for action in plan:
        state = dict(state)
        state["cols"] = dict(state["cols"])
        if (action[0] == "MOVE"):
            newPosition = int(action[3][4:])
            state["pos"] = newPosition
        if (action[0] == "FILLCONTAINER"):
            if action[3] == "CONTAINER0":
                state["c1"] = int(action[4][5:])
            else:
                state["c2"] = int(action[4][5:])
        if (action[0] == "PAINT"):
            state["cols"][state["pos"]] = int(action[3][5:])
            if action[4] == "CONTAINER0":
                state["c1"] = -1
            else:
                state["c2"] = -1
        states.append(state)
    return states

if len(sys.argv) < 2:
    print("Usage: simulate.py <problem-file> <plan-file>")
    exit()

problemFile = sys.argv[1]
planFile = sys.argv[2]
main()