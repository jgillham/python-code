import math
class Graph:
    nodes = list()
    links = list()
    #===================================NODE===================================#
    # XPos                -----      X position of the node
    # Ypos                -----      Y position of the node
    # theta(optional)     -----      angle to grab puck(optional)
    # puck(optional)      -----      1-16 representing which puck it can reach (optional)
    #===================================NODE===================================#
    class Node:
            def __init__(self, XPos, YPos):
                    self.X = XPos
                    self.Y = YPos
                    self.theta = None
                    self.puck = 0
    #===================================LINK===================================#
    # node1               -----      node from
    # node2               -----      node to
    # log (optional)      -----      binary 1/0 if there is/is not a log (optional)
    # theta (optional)    -----      the direction a bot must face while moving (optional)
    # length              -----      length of the link is set automatically
    #===================================LINK===================================#
    class Link:
        def __init__( self, node1, node2):
                logOffset = 0 # edit this to change percieved length of link due to a log
                self.node1=node1
                self.node2=node2
                self.log = 0
                self.theta = None
                self.length=math.hypot(node1.X-node2.X,node1.Y-node2.Y)+self.log*logOffset

    def addNode(self, x, y):
        self.nodes.append(self.Node(x,y))

    def addLink(self, node1, node2):
        self.links.append(self.Link(node1,node2))

    def removeNode(self, node):
        linksRemoved=0
        for link in self.links:
            if link.node1 == node or link.node2 == node:
                self.links.remove(link)
                self.removeNode(node)
                linksRemoved+=1
                break
        if linksRemoved==0:
            self.nodes.remove(node)
