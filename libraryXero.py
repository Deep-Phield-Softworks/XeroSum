#!/usr/bin/env python

from time import time
import xeroConstants
import os

#Given: a radius, center sector, MAPX, MAPY
#Return: a dict with section names as keys. The values
#will be the  (MAPX,MAPY) values under the radius
def area(radius, originSector, MAPX, MAPY):
    #If originSector arguement is an section instance..
    #if isinstance(originSector, section):
    #    origin = originSector.name #origin == that section's key string
    #else: #Otherwise originSector better be a db key string already
    #    origin = originSector 
    #Create the empty dict
    sectors = dict()
    origin = originSector
    #And fill it with empty lists to store tiles
    
    MAPX = 0
    MAPY = 0
    radius = 1
    xyVals = range(16) * 3
    
    iY = 16 + MAPY
    lowY = iY - radius
    highY = iY + radius
        
    iX = 16 + MAPX
    lowX = iX - radius
    highX = iX + radius
    
    yVals = []
    yLast = 0
    if lowY <= 16:
        yCrossed = 0
    else:
        yCrossed = 1
    sections = [[[],[],[]],[[],[],[]],[[],[],[]]]
    for iY in range(lowY,(highY+1)):
        if (yLast >= xyVals[iY]):
                yCrossed += 1
        xVals = []
        xLast = 0
        if lowX <= 16:
            xCrossed = 0
        else:
            xCrossed = 1
        xSects = [[],[],[]]
        for iX in range(lowX,(highX+1)):
            if (xLast >= xyVals[iX]):
                xCrossed += 1
            sections[yCrossed][xCrossed].append([xyVals[iX],xyVals[iY]])
    temp = []
    for y in sections:
        for x in y:
            temp.append(x)
    c = 0
    for key in calcSections(origin):
        sectors[key] = temp[c]
        c += 1
    return sectors

#Return current working directory that stores game .png image files
def getArtDir():
    artdir = os.getcwd() + os.sep + "pngs" + os.sep
    return artdir


#Code snippet from StackOverflow to make timestamp string
def timeString():
    ts = time() #Time in epoch seconds. Yay
    st = datetime.datetime.fromtimestamp(ts).strftime('%H%M%S_%Y-%m-%d')
    return st

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

#The checkBoundaries function keeps the view surface from going outside the
#bounds of its parent surface(map_surface).
####Possibly Deprecated due to method viewInBoundsCheck####
def checkBoundaries(corner):
    if corner[0] < xeroConstants.boundLeft:
        corner[0] = xeroConstants.boundLeft
    
    if corner[0] >= xeroConstants.boundRight:
        corner[0] = xeroConstants.boundRight
    
    if corner[1] < xeroConstants.boundTop:
        corner[1] = xeroConstants.boundTop
    
    if corner[1] >= xeroConstants.boundBottom:
        corner[1] = xeroConstants.boundBottom
    return corner

#Make a db key string
def dbKeyString(x, y):
    return "sect_" + str(x) + "_" + str(y)
    
#Make an xy coordinate from db key
def dbKeyStringToXY(key):
    list = key.split("_")
    x = list[1]
    y = list[2]
    return [int(x),int(y)]
    
#Given: DMXY == [x,y] in Dijkstra Map with values between 0-47
#       center == DB key string, like "sect_0_0"
#Return: sectorXY == ["sect_0_0",x,y] with x,y values between 0-15      
def dijkstraToSector(DMXY, center):
    sectorXY = []
    c = dbKeyStringToXY(center) #Change the db key center to sector x,y
    #For convenience reassign DMXY to x and y
    x = DMXY[0]
    y = DMXY[1]
    if x <= 15:     #If x is less than or equal to 15... 
        c[0] -= 1 #sector center x value -= 1
        nextX = x #Sector x value
    elif (x >= 32): #else if x >= 32...
        c[0] += 1 #sector center x value += 1
        nextX = x - 32
    else:
        nextX = x - 16
    if y <= 15:     #If y is less than or equal to 15... 
        c[1] -= 1 #sector center y value -= 1
        nextY = y #Sector y value
    elif (y >= 32): #else if y >= 32...
        c[1] += 1 #sector center y value += 1
        nextY = y - 32
    else:
        nextY = y - 16
    #Put the sector of the point in sectorXY variable for return
    sectorXY.append(dbKeyString(c[0], c[1]))
    sectorXY.append(nextX)
    sectorXY.append(nextY)
    return sectorXY

#Given: sectorXY == ["sect_0_0",x,y] with x,y values between 0-15 
#       center == DB key string, like "sect_0_0"
#Return:  DMXY == [x,y] in Dijkstra Map with values between 0-47
def sectorToDijkstra(sectorXY, center):
    c = dbKeyStringToXY(center) #Change the db key center to sector x,y mods
    s = dbKeyStringToXY(sectorXY[0]) #Change the sector db key to sector x,y mods
    dx = sectorXY[1]
    dy = sectorXY[2]
    #If sector x == center x... 
    if s[0] == c[0]:
        dx += 16 #Add 16 to dx
    #If sector x > center x...    
    elif s[0] > c[0]:
        dx += 32 #Add 32 to dx
    #Implied else is to leave dx alone (for leftmost sectors)
    #If sector y == center y... 
    if s[1] == c[1]:
        dy += 16 #Add 16 to dy
    #If sector y > center y...    
    elif s[1] > c[1]:
        dy += 32 #Add 32 to dy
    #Implied else is to leave dy alone (for bottom most sectors)
    return [dx,dy]
    
    