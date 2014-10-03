#!/usr/bin/env python

###Tile Variables###
#For isometric view, tile width should be twice tile height.
TILE_WIDTH   = 64
TILE_HEIGHT  = 32

###########UNBOUND METHODS###################
#Given:  List of ints
#Return: String for use as a dictionary key in form: "x_y_z"
def makeKey(XYZ):
    key = str(XYZ[0])
    for n in XYZ[1:len(XYZ)]:
        key = key + "_" + str(n)
    return key

#Given:  String in form: "int_int_int"
#Return: List of ints
def keyToXYZ(key):
    XYZ = [int(i) for i in key.split('_')]
    return XYZ

#Given: String in form: "int_int_int"
#Return: Parent chunk key string in form: "intX_intY_intZ"
def findParent(coordKey):
    XYZ = keyToXYZ(coordKey)
    parentChunk = makeKey([int(XYZ[0]/16),
                           int(XYZ[1]/16),
                           int(XYZ[2])] )
    return parentChunk

#Given: (x,y) of a mouse click
#Determine if the click is within a tile shaped diamond
def within(rect, point, width = TILE_WIDTH, height = TILE_HEIGHT):
    bool = False
    #4 points that define the rhombus
    A = rect.midleft#(x,(y + (height/2)) )           #9 O'clock
    B = rect.midbottom#((x + (width/2)),(y + height))  #6 O'clock
    C = rect.midright#((x + width),(y + (height/2))) #3 O'clock
    D = rect.midtop#((x + (width/2)),y)             #12 O'clock 

    if (leftOf(A,D,point) > 0):
        if (leftOf(B,C,point) < 0):
            if (leftOf(D,C,point) > 0):
                if (leftOf(A,B,point) < 0):
                    bool = True
    return bool

#Given: 2 points that for a line segment and a third point
#Determine if the third point is:
#-"left and/or above" the line (returns a positive integer),
#-"on the line" (returns 0), or
#-"right and/or below" the line (returns a negative integer)
def leftOf(one, two, point):
    X1 = one[0]
    X2 = two[0]
    Y1 = one[1]
    Y2 = two[1]
    Px = point[0]
    Py = point[1]
    left = (X2 - X1)*(Py - Y1) - (Y2 - Y1)*(Px - X1)
    return left

###########UNBOUND METHODS###################