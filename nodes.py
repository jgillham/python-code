import pygame, sys, math, graph, edit, random
from pygame.locals import *

if __name__ == "__main__":
    graph = graph.Graph()
    dummy = graph.addNode(-10,-10)
    pygame.init()
    screen=pygame.display.set_mode((960,960),0,32)
    pose = (0,0,0)
    drawFlag = 1

def drawObjects():
        blocks = [(273,235,34,34),(960-34,183,34,34),(253,591,34,34),(755,723,34,34)]
        circles = [(180,880),(470,590),(480,120)]
        lines = ((3,375,273,8),(273,9,373,358),(426,132,656,4),(372,172,706,499),(648,256,446,513),(303,372,300,686),(530,705,5,530))
        radiusCan=33
        colorCan=(139,137,137) #RGB
        colorWood=(160,82,45) #RGB
        colorLine=(150,150,100) #RGB
        gridColor=(0,105,0) #RGB

        screen.fill((200,200,200))
        for i in range(1,4):
            pygame.draw.line(screen,gridColor,(0,i*240),(960,i*240),1)
            pygame.draw.line(screen,gridColor,(i*240,0),(i*240,960),1)
        for block in blocks:
            pygame.draw.rect(screen, colorWood, block)
        for circle in circles:
            pygame.draw.circle(screen, colorCan, circle, radiusCan)
        for line in lines:
            pygame.draw.line(screen,colorLine, (1.357*line[0],1.357*line[1]),(1.357*line[2],1.357*line[3]), 20)
        drawBot(pose[0], pose[1], pose[2])

def drawBotTempPath():
    pygame.draw.line(screen, (255,0,0), (child[0],child[1]), (nodes[child[3]][0],nodes[child[3]][1]), 2)

def drawBot(x,y,theta):
        theta = theta * math.pi/180
        pygame.draw.polygon(screen, (245,245,245), ((x+60*math.cos(theta)-60*math.sin(theta),y-60*math.sin(theta)-60*math.cos(theta)),(x-60*math.cos(theta)-60*math.sin(theta),y+60*math.sin(theta)-60*math.cos(theta)),(x-60*math.cos(theta)+60*math.sin(theta),y+60*math.sin(theta)+60*math.cos(theta)),(x+60*math.cos(theta)+60*math.sin(theta),y-60*math.sin(theta)+60*math.cos(theta))), 3)
        pygame.draw.line(screen,(245,245,245), (x,y),(x-60*math.sin(theta),y-60*math.cos(theta)),3)

def whatNode((x,y)):
    nearestNode=graph.nodes[0]
    distance=960**2
    distanceLowest = 960**2

    for node in graph.nodes:
        distance = math.hypot(x-node.X,y-node.Y)
        if distance<distanceLowest:
            nearestNode=node
            distanceLowest=distance
    return (nearestNode, distanceLowest)

def drawGraph():
    for node in graph.nodes:#draw nodes
        if 0<=node.puck<=15:
            pygame.draw.circle(screen,(int(255*float(node.puck)/15),0,int(255-255*float(node.puck)/15)),(node.X,node.Y), node.radius)
            pygame.draw.circle(screen,(0,0,0),(node.X,node.Y), node.radius,1)
        else:
            pygame.draw.circle(screen,(100,255,255),(node.X,node.Y), node.radius)
            pygame.draw.circle(screen,(0,0,0),(node.X,node.Y), node.radius,1)
      #  if not (nodes[i][2] == -1):
       #     pygame.draw.line(screen,(255,100,50),(nodes[i][0],nodes[i][1]),(nodes[i][0]+radiusNode*2*math.sin(nodes[i][2]),nodes[i][1]+radiusNode*2*math.cos(nodes[i][2])),1)
    for link in graph.links:#draw links
        print "node1 = " + str(link.node1.X+link.node1.Y) + "    node2 = " + str(link.node2.X+link.node2.Y)
        pygame.draw.line(screen, (0,100,155), (link.node1.X,link.node1.Y),(link.node2.X,link.node2.Y),2)


def drawAll():
    screen.lock()
    drawObjects()
    drawGraph()
    screen.unlock()
    pygame.display.update()

def makeTimer( seconds ):
    """
    Makes a lambda function which returns true while their is time remaining.

    @param seconds is the number seconds to return true.

    @return a lambda function thats true while for number of seconds.

    Example
    >>> import time
    >>> timer = makeTimer( 0.100 )
    >>> timer()
    True
    >>> startTime = time.time()
    >>> while timer() and startTime + 0.200 > time.time():
    ...     pass
    >>> timer()
    False
    """
    import time
    startTime = time.time()
    return lambda : time.time() - startTime < seconds

# By default accept all mouse up events.
ignoreNextMouseUpEvent = lambda: False
while  __name__ == "__main__":
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Ignore mouse up events.
        if ignoreNextMouseUpEvent() and ( event.type == pygame.MOUSEBUTTONDOWN \
         or event.type == pygame.MOUSEBUTTONUP ):
            print "ignore mouse Up"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            posDown=pygame.mouse.get_pos()
            downNode=whatNode(posDown)[0]
            #note which node it is in
            drawFlag = 1


        elif event.type == pygame.MOUSEBUTTONUP:
            print "mouse Up"
            posUp = pygame.mouse.get_pos()
            upNode = whatNode(posUp)[0]
            #if in the same node, then:
            drawFlag = 1

            clickTravel = math.hypot(posDown[0]-posUp[0],posDown[1]-posUp[1])

            if whatNode(posDown)[1] <= downNode.radius:   #if click was inside a node
                print "what node is returning " + str(whatNode(posDown)[0])
                if whatNode(posUp)[1] <= upNode.radius:  #and  unclick was inside a node
                    if downNode==upNode:  #and those were the same nodes
                        right_mouse=pygame.mouse.get_pressed()
                        print right_mouse
                        if right_mouse[2] == 1:
                                drawFlag=0
                                while 1:
                                    if edit.editNode(upNode):
                                            drawAll()
                                    else:
                                            break
                                # Ignore mouse clicks for the next 150 ms
                                ignoreNextMouseUpEvent = makeTimer(0.150)
                        else:
                                graph.removeNode(whatNode(posDown)[0])  #remove that node
                    else: # but if they were two different nodes
                        graph.addLink(downNode, upNode)#then make a link between
                else:#clicked in a node, and dragged
                        downNode.X = posUp[0]
                        downNode.Y = posUp[1] #drag node

            else: # clicked not on a node
                if clickTravel <= downNode.radius: #clicked and didnt drag
                        graph.addNode(posDown[0], posDown[1])#add a node
                elif clickTravel > downNode.radius: #clicked and dragged
                        pose = ( posDown[0], posDown[1], 180/math.pi*math.atan2((posDown[0]-posUp[0]),(posDown[1]-posUp[1])) ) #drop bot on this node

    if drawFlag ==1:
        drawAll()
        drawFlag=0

def generateNode(node,end):
    """
    Generates a node that is closer to the end node. If the end node is close 
     enough, the generated node is the end node.

    Examples:
    >>> first = ( 0, 1 )
    >>> last = ( 100, 50 )
    >>> oldDistance = math.hypot( last[0] - first[0], last[1] - first[1] )
    >>> next = generateNode( first, last )
    >>> newDistance  = math.hypot( last[0] - next[0], last[1] - next[1] )
    >>> oldDistance > newDistance
    True
    >>> generateNode( (0,1), (100,50) )
    (100, 50)
    """
    parent = node
    distanceShortest = 10**11
    for i in range(100):
        x,y = node[0],node[1] #starting point
        oldDistance = math.hypot(x-end[0],y-end[1])
        r=random.gauss(60,5) # add 1 foot
        if oldDistance<120:
            r=oldDistance
        #rBest=r
        theta = random.randint(0,360)
        #thetaBest=theta
        newX=x+r*math.cos(math.pi/180*theta)
        newY=y+r*math.sin(math.pi/180*theta)
        distance=math.hypot(newX-end[0],newY-end[1]) #distance to end

        #for line in lines:
        #    if math.hypot(x+r*math.cos(math.pi/180*theta)-line[0],y+r*math.sin(math.pi/180*theta)-line[1])<=105:
        #        distance+=10**10
        for circle in circles:
            if math.hypot(x+r*math.cos(math.pi/180*theta)-circle[0],y+r*math.sin(math.pi/180*theta)-circle[1])<=105:
                distance+=10**10
            distance += 10**2/math.hypot(x+r*math.cos(math.pi/180*theta)-circle[0],y+r*math.sin(math.pi/180*theta)-circle[1])**2
        for block in blocks:
            if math.hypot(x+r*math.cos(math.pi/180*theta)-block[0],y+r*math.sin(math.pi/180*theta)-block[1])<=105:
                distance+=10**10
            distance += 10**2/math.hypot(x+r*math.cos(math.pi/180*theta)-block[0]+17,y+r*math.sin(math.pi/180*theta)-block[1]+17)**2
       # distance += 100/abs(newX-960)**2 + 100/abs(newX-0)**2 + 100/abs(newY-0)**2 + 100/abs(newY-960)**2
        if abs(newX-960)<80 or abs(newX-0)<80:
            distance+=10**10
        if abs(newY-960)<80 or abs(newY-0)<80:
            distance+=10**10

        if distance<distanceShortest:
            rBest=r
            thetaBest=theta
            distanceShortest=distance
    return(x+rBest*math.cos(math.pi/180*thetaBest),y+rBest*math.sin(math.pi/180*thetaBest))


def penalizeBranch(index,penalty):
    nodes[index][2]+=penalty #penalty
    for i in range(1,len(nodes)):
        nodes[index][2]+=penalty #penalty
        if nodes[i][3]==index:
            penalizeBranch(i, penalty)
def generatePath( path, start, end ):
    """
    Generates a path from the start to the end.

    Example:
    >>> path = generatePath( [], (0,0), (100,100) )
    >>> path[0]
    (0, 0)
    >>> path[-1]
    (100, 100)
    """
    if len(path) == 0:
        path.append( start )
    first = path[-1]
    last = generateNode( first, end )
    path.append( last )
    if math.hypot(last[0]-end[0],last[1]-end[1])>10:
        return generatePath( path, last, end )
    else:
        return path
