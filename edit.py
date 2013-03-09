import easygui
from easygui import *
import sys

def editNode(node):
    if node.theta == None:
        node.theta=0

    msg = "Node " + str(node)
    title = "Edit node " + str(node) +"'s data"
    fieldNames = ["X position", "Y position", "theta to grab puck at", "puck it can access 1-16"]
    fieldValues = [node.X,node.Y,node.theta,node.puck]  # we start with blanks for the values
    fieldValues = multenterbox(msg,title, fieldNames, fieldValues)
    if fieldValues == None:
        return False
    node.X = int(fieldValues[0])
    node.Y = int(fieldValues[1])
    node.theta = int(fieldValues[2])
    node.puck = int(fieldValues[3])
    return True
