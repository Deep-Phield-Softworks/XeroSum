#!/usr/bin/env python
from xeroConstants import *
import libraryXero as lib
#An object class to manage the points for a figure to move along
#Given: initial == list containing ["sector_0_0", x, y] of start point
#       center == a DB key string of the current center sector
#       goal == list containing ["sector_0_0", x, y] of path goal 
#Return self.path == list of [["sector_0_0", x, y], ... ] of the points to reach a goal
class path:
    def __init__(self, initial, center, goals):
        #print "####New Path####"
        self.goals = goals
        #print "Goals: ", self.goals
        self.center = str(center) 
        #print "Center: ", self.center
        self.initial = initial
        #print "Initial: ", self.initial
        self.DMAP = self.makeDMAP()
        self.dGoals = [lib.sectorToDijkstra(goal, self.center) for goal in self.goals]
        #print "dGoals: ", self.dGoals
        self.dInitial = lib.sectorToDijkstra(self.initial, self.center)
        #print "dInitial: ", self.dInitial
        self.DMAP = self.calcDMAP(self.dGoals)
        self.dPath = self.makeDijkstraPath(self.dInitial, self.DMAP)
        #print "dPath: ", self.dPath
        self.path = [lib.dijkstraToSector(node,self.center) for node in self.dPath]
        #print "path: ", self.path
        self.stepIndex = 0
        self.facings = self.createFacingArray(self.dPath)
        self.facing = 5
        
    
    #Move the path step index forward one node
    #Return a boolean of whether there was another step
    def advance(self):
        more = True
        self.stepIndex += 1
        if self.stepIndex >= len(self.path):
            more = False
            self.stepIndex -= 1
        return more
    
    #Use the self.dPath's "absolute" values to calculate facing
    #info at each step index
    def createFacingArray(self, dPath ):
        facings = []
        #If there is more than one node in path...
        if (len(dPath)) > 1:
            start = dPath[0] #set start node
            #foreach node in range...
            for node in range(1,len(dPath)):
                #compare the x and y values
                x1 = start[0]
                y1 = start[1]
                x2 = dPath[node][0]
                y2 = dPath[node][1]
                #Must use isometric headings here
                if x1 == x2:
                    if y2 < y1: #Heading SW
                        face = 1
                    else: #if y2 > y1 Heading NE
                        face = 9
                elif x1 < x2:
                    if y2 < y1: #Heading Due E
                        face = 6
                    elif y2 == y1: #Heading SE
                        face = 3
                    else: #Heading Due S
                        face = 2
                else: #if x1 > x2
                    if y2 < y1: #Heading Due N
                        face = 8
                    elif y2 == y1: #Heading NW
                        face = 7 
                    else: #Heading Due W
                        face = 4
                        
                facings.append(face)    
                start = dPath[node]
        facings.append(5)
        return facings
    
    #Create a fresh Dijkstra Map
    def makeDMAP(self):
        #Dijkstra Maps Constants
        SECTORS_WIDTH = 48
        SECTORS_HEIGHT = 48
        DMAP = []
        for x in range (SECTORS_WIDTH):
            DMAP.append([])
            for y in range (SECTORS_HEIGHT):
                DMAP[x].append([])
                DMAP[x][y] = [10000,False,0]
        return DMAP
    
    def makeDijkstraPath(self, start, MAP):
        path = [start]
        next = self.findNextNode(start, MAP)
        while (next != None):
            next = self.findNextNode(path[-1], MAP)
            if next != None:
                path.append(next)
        return path
    
    #Given: initial xy == dijkstra map xy as [x,y]
    def findNextNode(self, xy, MAP):
        next = None
        #Changing mods order to try and make diagonals "float to top"
        mods = [(0,-1),(-1,0),(1,0),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]
        lowestNeighbor = MAP[xy[0]][xy[1]][0]
        for mod in mods:
            adjX = xy[0] + mod[0]
            adjY = xy[1] + mod[1]
            if (adjX >= 0 and adjX <= (len(MAP)-1)) and (adjY >= 0 and adjY <= (len(MAP)-1)):
                if lowestNeighbor > MAP[adjX][adjY][0]:
                    next = [adjX,adjY]
                        
        return next
    
    #Given:  DMAP == a two dimensional list to store Dijkstra Map results
    #        goals == list of [x,y] values in Dijkstra Map format with at
    #                 least one entry.
    #Return: A processed Dijkstra map for the given goal(s) 
    def calcDMAP(self, goals):
        DMAP = self.makeDMAP()
        for goal in goals:
            x = goal[0]
            y = goal[1]
            DMAP[x][y] = [0,False,0]
        #For first pass set escape boolean to true
        changed = True
        #Make a list of modifiers to describe adjacent coordinates           
        mods = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]
        while (changed): #Until changed == False...
            changed = False #At start of loop changed == False
            for x in range(len(DMAP)): #At the start of the loop, check for values
                for y in range(len(DMAP[x])): #that need to be changed
                    if DMAP[x][y][1]: #If DMAP[x][y][1] == True, then  
                        DMAP[x][y][1] = False #set it back to false and 
                        DMAP[x][y][0] = DMAP[x][y][2] + 1 #set DMAP[x][y][0] == to lowest neighbor + 1 
            for x in range(len(DMAP)): 
                for y in range(len(DMAP)): 
                    #Initialize the lowest neighbor
                    #The modified index values are negative for some cases, this appears to be a
                    #benign error at the moment
                    lowestNeighbor = DMAP[x + mods[0][0]][y + mods[0][1]][0]
                    for mod in mods:
                        adjX = x + mod[0]
                        adjY = y + mod[1]
                        if (adjX >= 0 and adjX <= (len(DMAP[x])-1)) and (adjY >= 0 and adjY <= (len(DMAP[x])-1)):
                            if lowestNeighbor > DMAP[adjX][adjY][0]:
                                lowestNeighbor = DMAP[adjX][adjY][0]
                    #If any DMAP[x][y][0] is at least 2 greater than its lowest neighbor...
                    #set it to 1 greater than the lowest value neighbor
                    if (DMAP[x][y][0] - lowestNeighbor) >= 2:
                        DMAP[x][y][1] = True
                        DMAP[x][y][2] = lowestNeighbor
                        changed = True
        ###Uncomment to print DMAP values
        #temp = self.makeDMAP()
        #for x in range(len(DMAP)):
        #    for y in range(len(DMAP[x])):
        #        temp[x][y] = DMAP[x][y][0]
        #print temp
        return DMAP
        
    
    
