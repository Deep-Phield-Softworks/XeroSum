#!/usr/bin/env python
from AoE import *
from unboundMethods import *

#Djikstra Map objects that can be combined together and can find paths
#Given:
#-shape, a shape template object from AoE.py
#-selectedDict, a dictionary of coordinate Keys as dict keys and values that
# will be added to the DMAP
#Return: a Djikstra Map object that:
#-can be combined with other Djikstra Maps
#-should be processed once all desired input DMAPs have been combined
#-can return a list of nodes using findPath(start) 

class DjikstraMap:
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
        for key in self.keysFlatList:
            if DMAP.MapVals.has_key(key):
                if DMAP.MapVals[key] == None or self.MapVals[key] == None:
                    self.MapVals[key] = None
                else:
                    self.MapVals[key] = self.MapVals[key] + DMAP.MapVals[key]
        return self
    
if __name__ == '__main__':
    origin = [0,0,0]
    test = 'test'
    oKey = makeKey(origin)
    shape = Cube(oKey, [21,21,1], True)
    selectedDict = dict()
    selectedDict['10_10_0'] = 0
    selectedDict['1_1_0']   = None
    
    d = DjikstraMap(shape, selectedDict)
    d.processMap()
    print d.findPath('0_0_0')