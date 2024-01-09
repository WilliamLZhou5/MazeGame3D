import pygame
import math
import random

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0

# make walls
grid = pygame.Vector2(50,50)
wallThickness = 10
wallsV = [[pygame.Rect((grid.x*a-wallThickness/2, grid.y*b-wallThickness/2, wallThickness, grid.y+wallThickness)) for a in range(math.floor(SCREEN_WIDTH/grid.x) + 1)] for b in range(math.floor(SCREEN_HEIGHT/grid.y) + 1)]
wallsH = [[pygame.Rect((grid.x*a, grid.y*b-wallThickness/2, grid.x+wallThickness/2, wallThickness)) for a in range(math.floor(SCREEN_WIDTH/grid.x) + 1)] for b in range(math.floor(SCREEN_HEIGHT/grid.y) + 1)]

# get random starting position
startBlockX = random.randint(0,11)
startBlockY = random.randint(0,11)
startBlock = pygame.Rect((startBlockX*50, startBlockY*50,50,50))
print("Start here: (", startBlockX, ",", startBlockY, ")")

viewWidth = math.radians(140)
playerSize = 10
player = pygame.Rect((startBlockX*grid.x+grid.x/2-playerSize/2, startBlockY*grid.y+grid.y/2-playerSize/2,playerSize,playerSize))

# make maze
visitedGrids = [[False for a in range(math.floor(SCREEN_WIDTH/grid.x))] for b in range(math.floor(SCREEN_HEIGHT/grid.y))]
visitedGrids[startBlockX][startBlockY] = True
currentPos = pygame.Vector2(startBlockX,startBlockY)
counter = 0

# gets the corner of a wall
def cornerOfWalls(wall , corner, currPos, n):
    delta = 0.05
    # 0 top left, 1 top right, 2 bottom right, 3 bottom left
    loc = 0
    if corner == 0:
        loc = pygame.Vector2(wall.x, wall.y)
        if n == 0:
            loc.x -= delta
        if n == 2:
            loc.y -= delta
    if corner == 1:
        loc = pygame.Vector2(wall.x + wall.width, wall.y)
        if n == 0:
            loc.x += delta
        if n == 2:
            loc.y -= delta
    if corner == 2:
        loc = pygame.Vector2(wall.x + wall.width, wall.y + wall.height)
        if n == 0:
            loc.x += delta
        if n == 2:
            loc.y += delta
    if corner == 3:
        loc = pygame.Vector2(wall.x, wall.y + wall.height)
        if n == 0:
            loc.x -= delta
        if n == 2:
            loc.y += delta
    
    # This stuff keeps the rays within the viewAngle
    angle = 0
    if loc.x == currPos.x:
        if loc.y > currPos.y:
            angle = math.pi/2
        else:
            angle = -math.pi/2
    else:
        angle = math.atan((loc.y-currPos.y)/(loc.x-currPos.x))
    
    if loc.x < currPos.x:
        angle += math.pi
    
    if viewAngle + viewWidth/2 >= math.pi*2:
        if angle%(math.pi*2)  >= (viewAngle-viewWidth/2) or angle%(math.pi*2) <= (viewAngle + viewWidth/2)%(math.pi*2):
            return loc
    if viewAngle - viewWidth/2 <= 0:
        if angle%(math.pi*2) <= (viewAngle+viewWidth/2)%(math.pi*2) or angle%(math.pi*2) >= (viewAngle - viewWidth/2)%(math.pi*2):
            return loc 
    if angle%(math.pi*2) <= (viewAngle + viewWidth/2)%(math.pi*2) and angle%(math.pi*2) >= (viewAngle - viewWidth/2)%(math.pi*2):
        return loc
    return -1

def findIntersections(cornerPos, currPos):
    intersections = []
    for i in range(math.floor(currXY.x-2), math.floor(currXY.x+3)):
        for l in range(math.floor(currXY.y-2), math.floor(currXY.y+3)):
            if l < 0:
                continue
            if i < 0: 
                continue
            if l > len(wallsH) - 1:
                continue
            if i > len(wallsH[l]) - 1:
                continue
            j = wallsH[l][i]
    # for i in wallsH:
    #     for j in i:
            for k in range(4):
                if not j == -1:
                # 0 is top, 1 is right, 2 is down, 3 is left
                    line = 0
                    yInt = 0
                    xInt = 0
                    direction = ""
                    if k == 0:
                        direction = "horizontal"
                        line = j.y
                    if k == 1:
                        direction = "vertical"
                        line = j.x + j.width
                    if k == 2:
                        direction = "horizontal"
                        line = j.y + j.height   
                    if k == 3:
                        direction = "vertical"
                        line = j.x

                    m = 0
                    if cornerPos.x == currPos.x:
                        m == "DNE"
                    else: 
                        m = (cornerPos.y-currPos.y)/(cornerPos.x-currPos.x)

                    if direction == "horizontal":
                        if cornerPos.y == currPos.y:
                            continue
                        poi = (line - currPos.y)*(cornerPos.x - currPos.x)/(cornerPos.y - currPos.y)+ currPos.x
                        if pygame.Vector2.magnitude_squared(currPos-pygame.Vector2(poi,line)) > 22500:
                            continue
                        if poi < j.x + j.width and poi > j.x:
                            intersections.append(pygame.Vector2(poi,line))
                
                    if direction == "vertical":
                        if cornerPos.x == currPos.x:
                            continue
                        poi = (line - currPos.x)*(cornerPos.y - currPos.y)/(cornerPos.x - currPos.x) + currPos.y
                        if pygame.Vector2.magnitude_squared(currPos-pygame.Vector2(poi,line)) > 22500:
                            continue
                        if poi < j.y + j.height and poi > j.y:
                            intersections.append(pygame.Vector2(line, poi))

    for i in range(math.floor(currXY.x-2), math.floor(currXY.x+3)):
        for l in range(math.floor(currXY.y-2), math.floor(currXY.y+3)):
            if l < 0:
                continue
            if i < 0: 
                continue
            if l > len(wallsV) - 1:
                continue
            if i > len(wallsV[l]) - 1:
                continue
            j = wallsV[l][i]
    # for i in wallsV:
    #     for j in i:
            for k in range(4):
                if not j == -1:
                # 0 is top, 1 is right, 2 is down, 3 is left
                    line = 0
                    direction = ""
                    if k == 0:
                        direction = "horizontal"
                        line = j.y
                    if k == 1:
                        direction = "vertical"
                        line = j.x + j.width
                    if k == 2:
                        direction = "horizontal"
                        line = j.y + j.height   
                    if k == 3:
                        direction = "vertical"
                        line = j.x
                    m = 0
                    if cornerPos.x == currPos.x:
                        m == "DNE"
                    else: 
                        m = (cornerPos.y-currPos.y)/(cornerPos.x-currPos.x)

                    if direction == "horizontal":
                        if cornerPos.y == currPos.y:
                            continue
                        poi = ((line - currPos.y)*(cornerPos.x - currPos.x)/(cornerPos.y - currPos.y)) + currPos.x
                        
                        if poi <= j.x + j.width and poi >= j.x:
                            intersections.append(pygame.Vector2(poi,line))

                    if direction == "vertical":
                        if cornerPos.x == currPos.x:
                            continue
                        
                        poi = (line - currPos.x)*(cornerPos.y - currPos.y)/(cornerPos.x - currPos.x) + currPos.y
                        if poi <= j.y + j.height and poi > j.y:
                            intersections.append(pygame.Vector2(line, poi))
    return intersections

def getMinIntersection(cornerPos, currPos):
    allintersects = findIntersections(cornerPos, currPos)
    minLoc = pygame.Vector2(math.inf,math.inf)
    for i in allintersects:
        if pygame.Vector2.magnitude_squared(i-cornerPos) < pygame.Vector2.magnitude_squared(cornerPos-currPos) and pygame.Vector2.magnitude_squared(minLoc-currPos) > pygame.Vector2.magnitude_squared(i-currPos):
            minLoc.x = i.x
            minLoc.y = i.y
    return minLoc

def relativeAngle(cornerPos, currPos):
    if cornerPos.x == currPos.x:
        if cornerPos.y < currPos.y:
            return math.pi/4
        else:
            return 3*math.pi/4
    angle = math.atan((cornerPos.y-currPos.y)/(cornerPos.x-currPos.x))

    if cornerPos.x < currPos.x:
        angle += math.pi
    
    if angle < 0:
        angle+= 2*math.pi
    return angle

def sortCorners(corners, currPos):
    def sortAngles(corner, currPos):
        angle = relativeAngle(corner,currPos)
        if viewAngle + viewWidth/2 > math.pi*2 :
            if angle < viewWidth/2:
                angle += math.pi*2
        if viewAngle - viewWidth/2 < 0:
            if angle > math.pi*2-viewWidth/2:
                angle -= math.pi*2
        return angle
    return  sorted(corners, key = lambda x: sortAngles(x, currPos))

viewAngle = 0.0
velocityTotal = 0.9
velX = 0
velY = 0
centerLoc = pygame.Vector2(player.x + player.w/2, player.y + player.h/2)
showMap = False

def getMinCorners():
    corners = []
    for i in range(math.floor(currXY.x-2), math.floor(currXY.x+3)):
        for l in range(math.floor(currXY.y-2), math.floor(currXY.y+3)):
            if l < 0:
                continue
            if i < 0: 
                continue
            if l > len(wallsH) - 1:
                continue
            if i > len(wallsH[l]) - 1:
                continue
            j = wallsH[l][i]
    # for i in wallsH:
    #     for j in i:
            for k in range(4):
                if not j == -1:
                    for n in range(3):
                        if not cornerOfWalls(j, k, centerLoc, n) == -1:
                            if not getMinIntersection(cornerOfWalls(j, k, centerLoc ,n),centerLoc).x > SCREEN_WIDTH + 100:
                                corners.append(getMinIntersection(cornerOfWalls(j, k, centerLoc, n),centerLoc))

    for i in range(math.floor(currXY.x-2), math.floor(currXY.x+3)):
        for l in range(math.floor(currXY.y-2), math.floor(currXY.y+3)):
            if l < 0:
                continue
            if i < 0: 
                continue
            if l > len(wallsV) - 1:
                continue
            if i > len(wallsV[l]) - 1:
                continue
            j = wallsV[l][i]
    # for i in wallsV:
    #     for j in i:
            for k in range(4):
                if not j == -1:
                    for n in range(3):
                        if not cornerOfWalls(j, k, centerLoc, n) == -1:
                            if not getMinIntersection(cornerOfWalls(j, k, centerLoc, n),centerLoc).x > SCREEN_WIDTH + 100:
                                corners.append(getMinIntersection(cornerOfWalls(j, k, centerLoc, n),centerLoc))
    sorted = sortCorners(corners, centerLoc)
    return sorted

wallSegmentWidth = 15
def findPolygonPoints(corners, currPos):
    polygons = []
    for i in range(len(corners)-1):
        this = corners[i]
        next = corners[i+1]
        distThis = pygame.Vector2.magnitude(this-currPos)
        distNext = pygame.Vector2.magnitude(next-currPos)
        relAngleThis = relativeAngle(this,currPos)
        relAngleNext = relativeAngle(next,currPos)
        if viewAngle + viewWidth/2 > math.pi*2:
            if relAngleThis < viewWidth/2:
                relAngleThis += math.pi*2
            if relAngleNext < viewWidth/2:
                relAngleNext += math.pi*2
        if viewAngle - viewWidth/2 < 0:
            if relAngleThis > math.pi*2-viewWidth/2:
                relAngleThis -= math.pi*2
            if relAngleNext > math.pi*2-viewWidth/2:
                relAngleNext -= math.pi*2
        relAngleThis -= viewAngle
        relAngleNext -= viewAngle
        wallProportionThis = SCREEN_HEIGHT/2-distThis*2
        wallProportionNext = SCREEN_HEIGHT/2-distNext*2
        p1 = pygame.Vector2((SCREEN_WIDTH + 30)/2*(math.sin((math.pi*(relAngleThis+viewWidth/2)/viewWidth-math.pi/2))+1), (SCREEN_HEIGHT/2)-wallProportionThis)
        p2 = pygame.Vector2((SCREEN_WIDTH + 30)/2*(math.sin((math.pi*(relAngleThis+viewWidth/2)/viewWidth-math.pi/2))+1), SCREEN_HEIGHT/2+wallProportionThis)
        p3 = pygame.Vector2((SCREEN_WIDTH + 30)/2*(math.sin((math.pi*(relAngleNext+viewWidth/2)/viewWidth-math.pi/2))+1), SCREEN_HEIGHT/2-wallProportionNext)
        p4 = pygame.Vector2((SCREEN_WIDTH + 30)/2*(math.sin((math.pi*(relAngleNext+viewWidth/2)/viewWidth-math.pi/2))+1), SCREEN_HEIGHT/2+wallProportionNext)
        # p1 = pygame.Vector2((SCREEN_WIDTH + 30)*(relAngleThis+viewWidth/2)/viewWidth, (SCREEN_HEIGHT/2)-wallProportionThis)
        # p2 = pygame.Vector2((SCREEN_WIDTH + 30)*(relAngleThis+viewWidth/2)/viewWidth, SCREEN_HEIGHT/2+wallProportionThis)
        # p3 = pygame.Vector2((SCREEN_WIDTH + 30)*(relAngleNext+viewWidth/2)/viewWidth, SCREEN_HEIGHT/2-wallProportionNext)
        # p4 = pygame.Vector2((SCREEN_WIDTH + 30)*(relAngleNext+viewWidth/2)/viewWidth, SCREEN_HEIGHT/2+wallProportionNext)
        # if pygame.Vector2.magnitude(next-this) >= 40:
        #     polygons.append([p1,p2,p4,p3,1])
        # else:
        polygons.append([p1,p2,p4,p3])
    return polygons

def findColour(pTop, pBottom, pTop2, pBottom2):
    height = min(abs(pBottom.y - pTop.y), abs(pBottom2.y - pTop2.y))
    c = 10+100*height/600
    return pygame.Color((c,c,c))

def draw3d(currPos):
    screen.fill((0,0,255))
    pygame.draw.rect(screen,"grey",pygame.Rect((0 , SCREEN_HEIGHT/2, SCREEN_WIDTH,SCREEN_HEIGHT/2)))
    polygonPoints = findPolygonPoints(getMinCorners(), currPos)
    if not polygonPoints:
        pygame.draw.rect(screen, (110,110,110), pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
    else:
        for i in range(len(polygonPoints)):
        # if 1 in polygonPoints[i]:
        #     polygonPoints[i].pop()
        #     pygame.draw.polygon(screen, "white", polygonPoints[i])
        # else:
            colour = findColour(polygonPoints[i][0], polygonPoints[i][1], polygonPoints[i][2], polygonPoints[i][3])
            pygame.draw.polygon(screen, colour, polygonPoints[i])

def minimap():
    screen.fill((0,0,0))
    pygame.draw.rect(screen, "blue", startBlock)
    pygame.draw.rect(screen, "green", endPoint)
    pygame.draw.rect(screen, (255,0,0), player)
    # show walls
    for i in wallsV:
        for j in i:
            if not j == -1:
                pygame.draw.rect(screen, "white", j)
    for i in wallsH:
        for j in i:
            if not j == -1:
                pygame.draw.rect(screen, "white", j)

    # for i in getMinCorners():
    #     pygame.draw.line(screen, (150,150,150), centerLoc, i)

    cornerArray = getMinCorners()
    for i in range(len(cornerArray)):
        pygame.draw.line(screen,(50+200*(i/len(cornerArray)),50+200*(i/len(cornerArray)),50+200*(i/len(cornerArray))), centerLoc, cornerArray[i])

while counter < 5000 and any(False in sublist for sublist in visitedGrids):
    counter+=1
    # 1 is up, 2 is right, 3 is down, 4 is left
    direction = random.randint(1,4)
    if direction == 1:
        # print("up")
        if currentPos.y == 0:
            continue
        currentPos.y -= 1
    elif direction == 2:
        # print("right")
        if currentPos.x == (math.floor(SCREEN_HEIGHT/grid.x)-1):
            continue
        currentPos.x += 1
    elif direction == 3:
        # print("down")
        if currentPos.y == (math.floor(SCREEN_HEIGHT/grid.y)-1):
            continue
        currentPos.y += 1
    else:
        # print("left")
        if currentPos.x == 0:
            continue
        currentPos.x -= 1

    # print(currentPos)
    # print(currentPos.x)
    # print(currentPos.y)
    if not visitedGrids[math.floor(currentPos.x)][math.floor(currentPos.y)]:
        # print("remove wall")
        # remove the correct wall, set visited to true
        visitedGrids[math.floor(currentPos.x)][math.floor(currentPos.y)] = True
        if direction == 1:
            wallsH[math.floor(currentPos.y) + 1][math.floor(currentPos.x)] = -1
        elif direction == 2:
            wallsV[math.floor(currentPos.y)][math.floor(currentPos.x)] = -1
        elif direction == 3:
            wallsH[math.floor(currentPos.y)][math.floor(currentPos.x)] = -1
        else:
            wallsV[math.floor(currentPos.y)][math.floor(currentPos.x) + 1] = -1
endPoint = pygame.Rect((math.floor(currentPos.x)*50, math.floor(currentPos.y)*50,50,50))
print("Count:" , counter)

run = True
while run:
    key = pygame.key.get_pressed()   
    centerLoc = pygame.Vector2(player.x + player.w/2, player.y + player.h/2)
    currXY = pygame.Vector2(math.floor((centerLoc.x)/grid.x), math.floor((centerLoc.y)/grid.y))

    # LINES TO EACH CORNER
    

    # camera move
    if key[pygame.K_d]:
        viewAngle += 0.05
    if key[pygame.K_a]:
        viewAngle -= 0.05
    if viewAngle >= 2*math.pi:
        viewAngle -= 2*math.pi
    elif viewAngle < 0:
        viewAngle += 2*math.pi

    velX = 0
    velY = 0
    # movement
    keyClicked = "W"
    if key[pygame.K_w]:
        velX = velocityTotal*math.cos(viewAngle)#*dt
        velY = velocityTotal*math.sin(viewAngle)#*dt
        keyClicked = "W"
    if key[pygame.K_s]:
        velX = -velocityTotal*math.cos(viewAngle)#*dt
        velY = -velocityTotal*math.sin(viewAngle)#*dt
        keyClicked = "S"

    # next potential pos
    if keyClicked == "W":
        nextPosX = player.x + velocityTotal*math.cos(viewAngle)#*dt
        nextPosY = player.y + velocityTotal*math.sin(viewAngle)#*dt
    elif keyClicked == "S":
        nextPosX = player.x - velocityTotal*math.cos(viewAngle)#*dt
        nextPosY = player.y - velocityTotal*math.sin(viewAngle)#*dt

    # check wall collision
    for i in range(math.floor(currXY.x-1), math.floor(currXY.x+2)):
        for k in range(math.floor(currXY.y-1), math.floor(currXY.y+2)):
            j = wallsV[k][i]
            if not j == -1:
                if player.width + nextPosX >= j.x and nextPosX <= j.x + j.width and player.height + nextPosY >= j.y and nextPosY <= j.y + j.height:
                    velX = 0
                    if player.y > j.y + j.height or player.y + player.height < j.y:
                        velY = 0
    for i in range(math.floor(currXY.x-1), math.floor(currXY.x+2)):
        for k in range(math.floor(currXY.y-1), math.floor(currXY.y+2)):
            j = wallsH[k][i]
            if not j == -1:
                if player.width + nextPosX >= j.x and nextPosX <= j.x + j.width and player.height + nextPosY >= j.y and nextPosY<= j.y + j.height:
                    velY = 0
                    if player.x > j.x + j.width or player.x + player.width < j.x:
                        velX = 0 
    
    player.x += velX
    player.y += velY

    if key[pygame.K_r]:
        player.x = startBlockX*grid.x+grid.x/2-playerSize/2
        player.y = startBlockY*grid.y+grid.y/2-playerSize/2
    
    counter +=1
    if key[pygame.K_m]:
        if counter > 10:
            showMap = not showMap
            counter = 0
        

    if showMap:
        minimap()
    else:
        draw3d(centerLoc)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

    clock.tick(60) / 1000
    
pygame.quit()