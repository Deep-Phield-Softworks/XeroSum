#!/usr/bin/env python
from aoe import *
from unboundmethods import *

#Djikstra Map objects that can be combined together and can find paths
#Given:
#-shape, a shape template object from AoE.py
#-selectedDict, a dictionary of coordinate Keys as dict keys and values that
# will be added to the DMAP
#Return: a Djikstra Map object that:
#-can be combined with other Djikstra Maps
#-should be processed once all desired input DMAPs have been combined
#-can return a list of nodes using findPath(start) 

class DijkstraMap:
    def __init__(self, shape, selectedDict, defaultMax = 10000):
        self.shape = shape
        self.selectedDict = selectedDict
        #The coordinate keys are already in shape...
        self.coordinates = self.shape.nDimensionalArray #Use shape's nD Key list
        #Create a dictionary to store the values
        self.keysFlatList = []
        self.MapVals = dict()
        #Populate the Map Values
        for x in range(0,len(self.coordinates)):
            for y in range(0,len(self.coordinates[x])):
                for z in range(0,len(self.coordinates[x][y])):
                        self.MapVals[self.coordinates[x][y][z]] = defaultMax
                        self.keysFlatList.append(self.coordinates[x][y][z])
        for key in self.selectedDict.keys():
            if self.MapVals.has_key(key):
                self.MapVals[key] = self.selectedDict[key] 
        #Using custom mods order to make diagonals "float to top" in paths
        self.mods = [(-1,-1,-1),(1,1,-1),(-1,1,-1),(1,-1,-1),(0,-1,-1),(-1,0,-1),(1,0,-1),(0,1,-1),
                     (-1,-1,0) ,(1,1,0), (-1,1,0), (1,-1,0), (0,-1,0), (-1,0,0), (1,0,0), (0,1,0), (0,0,0),
                     (-1,-1,1), (1,1,1), (-1,1,1), (1,-1,1), (0,-1,1), (-1,0,1), (1,0,1), (0,1,1)]
    #You should call this ONLY once all desired inputs have been combined into
    #one DMAP. It must be called before using findPath().
    def processMap(self):
        again = True #Control Boolean
        while(again): #Run at least once
            again = False #Set continue to false unless values change
            for key in self.keysFlatList:
                if self.MapVals[key] != None:
                    low = self.lowestNeighborValue(key)[0]
                    if low != None:
                        if (self.MapVals[key] - low)>= 2:
                            self.MapVals[key] = low + 1
                            again = True
    #Returns the tuple of info on lowest neighbor it can find.        
    def lowestNeighborValue(self, key):
        lowKey = None
        XYZ = keyToXYZ(key)
        for mod in self.mods:
            initial = [(XYZ[0] + mod[0]),(XYZ[1] + mod[1]),(XYZ[2] + mod[2])]
            trialKey = makeKey(initial)
            #Use lazy and eval to avoid "no such key" exception here
            if self.MapVals.has_key(trialKey) and self.MapVals[trialKey]!= None:
               low = self.MapVals[trialKey]
               lowKey = trialKey 
               break
        for mod in self.mods:
            lookup = [None, None, None]
            lookup[0] = XYZ[0] + mod[0]
            lookup[1] = XYZ[1] + mod[1]
            lookup[2] = XYZ[2] + mod[2]
            modKey = makeKey(lookup)
            if self.MapVals.has_key(modKey)and self.MapVals[modKey] != None:
                if self.MapVals[modKey] <= low:
                    low = self.MapVals[modKey]
                    lowKey = modKey
        return (low, lowKey)
            
    def findPath(self, startKey):
        nodes = [startKey]
        nextNode = self.lowestNeighborValue(nodes[-1])[1]
        while(nextNode != None):
            nextNode = self.lowestNeighborValue(nodes[-1])[1]
            if nextNode != nodes[-1]:
                nodes.append(nextNode)
            else:
                break
        return nodes

    #Add together the values of two DMAPS. If a given coordinate is None in
    #either DMAP it becomes None. Otherwise the values of both are added.
    def combine(self, DMAP):
        for key in self.keysFlatList: #For key in self..
            if DMAP.MapVals.has_key(key): #If key in DMAP...
                if DMAP.MapVals[key] == None or self.MapVals[key] == None:
                    self.MapVals[key] = None #Set value
                else:
                    self.MapVals[key] = self.MapVals[key] + DMAP.MapVals[key]
        return self
    
    #Combine two DMAPs. Then expand the calling DMAP by the unique coordinates
    #in the argument DMAP.
    def expand(self, DMAP):
        #First combine the cells they have in common
        self = self.combine(DMAP)
        #Add new keys from DMAP
        for key in DMAP.keysFlatList:  #For key in DMAP
            if not self.MapVals.has_key(key): #If key not in self
                self.MapVals[key] = DMAP.MapVals[key] #Add key & value to self
                self.keysFlatList.append(key)         #Add key to flat list
        #Lastly make a new expanded DMAP, populating the empty cells w/ None
        selfBounds = self.bounds() #Find the bounds
        DMAPBounds = DMAP.bounds() 
        origin = makeKey(self.lower(selfBounds, DMAPBounds)) #Find the origin
        magnitude  = (abs(selfBounds[0]-DMAPBounds[0]),
                      abs(selfBounds[1]-DMAPBounds[1]),
                      abs(selfBounds[2]-DMAPBounds[2])
                      )
        newShape = Cube(origin, magnitude, True) #Create a new Shape
        expanded = DijkstraMap(newShape, self.MapVals, None)
        return expanded
    
    #Define the bounaries as a pair of lowest (x,y,z) and greatest
    #(x,y,z) values as determiend by using the calling DMAP's self.coordinates
    def bounds(self):
        low = keyToXYZ(self.coordinates[0][0][0])
        hi  = keyToXYZ(self.coordinates[-1][-1][-1])
        return (low, hi)
    
    #Given two points in form: (x,y,z)
    #Return: Lower of the two points
    def lower(self, a, b):
        low = a
        if a[0] > b[0]:
            low = b
        elif a[1] > b[1]:
            low = b
        elif a[2] > b[2]:
            low = b
        return low
    
if __name__ == '__main__':
    #Run a test
    #Make a key to use in shape object creation
    origin = [0,0,0] 
    oKey = makeKey(origin) 
    #Make a Cube shape object
    shape = Cube(oKey, [21,21,1], True) #Shape will extend from (0,0,0) to (20,20,0) in cube shape
    #Dictionary of selected cells and their values.
    #Value of 0 is a goal, None is impassible
    selectedDict = dict()
    selectedDict['10_10_0'] = 0
    selectedDict['1_1_0']   = None
    #Create the Dijkstra Map
    d = DijkstraMap(shape, selectedDict)
    #Optionally Combine other DMAPs if desired
    #d.combine(otherDMAP)
    #After all DMAPs are combined, process once
    d.processMap()
    #Find a path given a start point
    print d.findPath('0_0_0')
    print "Bounds"
    print d.bounds()