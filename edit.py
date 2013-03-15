import easygui
from easygui import *
import sys

def editNode(node):
    msg = "Node " + str(node)
    title = "Edit node " + str(node) +"'s data"
    fieldNames = ["X position", "Y position", "theta to grab puck at", "puck it can access 0-15 (-1 for None)", "radius of acceptability"]
    fieldValues = [node.X,node.Y,node.theta,node.puck, node.radius]
    fieldValues = multenterbox(msg,title, fieldNames, fieldValues)
    if fieldValues == None:
        return False
    node.X = int(fieldValues[0])
    node.Y = int(fieldValues[1])
    node.theta = int(fieldValues[2])
    node.puck = int(fieldValues[3])
    node.radius = int(fieldValues[4])
    return True

def editLink(link):
    msg = "Link " + str(link)
    title = "Edit link " + str(link) +"'s data"
    fieldNames = ["log (0/1)", "directional (0/1)", "direction (degrees)", "length"]
    fieldValues = [link.log, link.directional, link.theta, link.length]
    fieldValues = multenterbox(msg,title, fieldNames, fieldValues)
    if fieldValues == None:
        return False
    link.log = int(fieldValues[0])
    link.directional = int(fieldValues[1])
    link.theta = int(fieldValues[2])
    link.length = int(fieldValues[3])
    return True

    
