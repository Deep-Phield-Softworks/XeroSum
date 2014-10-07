#!/usr/bin/env python
from AoE import *
from unboundMethods import *

class DjikstraMap:
    def __init__(self, shape, selectedKeys, setValue = 0):
        self.shape = shape
        self.selectedKeys = selectedKeys
        self.setValue = setValue
        #The coordinate keys are already in shape...
        self.coordinates = self.shape.nDimensionalArray #Use shape's nD Key list
        #Create a dictionary to store the values
        self.keysFlatList = []
        self.MapVals = dict()
        #Populate the Map Values
        for x in range(0,len(self.coordinates)):
            for y in range(0,len(self.coordinates[x])):
                for z in range(0,len(self.coordinates[x][y])):
                    self.MapVals[self.coordinates[x][y][z].key] = 10000
                    self.keysFlatList.append(self.coordinates[x][y][z].key)
        for key in self.selectedKeys:
            if self.MapVals.has_key(key):
                self.MapVals[key] = setValue #Set the goals to low values
        #Using custom mods order to try and make diagonals "float to top"
        self.mods = [(-1,-1,-1),(1,1,-1),(-1,1,-1),(1,-1,-1),(0,-1,-1),(-1,0,-1),(1,0,-1),(0,1,-1),
                     (-1,-1,0) ,(1,1,0), (-1,1,0), (1,-1,0), (0,-1,0), (-1,0,0), (1,0,0), (0,1,0), (0,0,0),
                     (-1,-1,1), (1,1,1), (-1,1,1), (1,-1,1), (0,-1,1), (-1,0,1), (1,0,1), (0,1,1)]
    def processMap(self):
        again = True #Control Boolean
        while(again): #Run at least once
            again = False #Set continue to false unless values change
            for key in self.keysFlatList:
                low = self.lowestNeighborValue(key)[0]
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
            if self.MapVals.has_key(trialKey):
               low = self.MapVals[trialKey]
               lowKey = trialKey 
               break
        for mod in self.mods:
            lookup = [None, None, None]
            lookup[0] = XYZ[0] + mod[0]
            lookup[1] = XYZ[1] + mod[1]
            lookup[2] = XYZ[2] + mod[2]
            modKey = makeKey(lookup)
            if self.MapVals.has_key(modKey):
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

    #Add together the values of two DMAPS
    def combine(self, DMAP):
        pass
if __name__ == '__main__':
    pass