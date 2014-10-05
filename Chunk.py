#!/usr/bin/env python
from unboundMethods import *
from Coordinate import Coordinate
#Chunk objects are containers for organizing coordinates into sets that are
#either active or inactive. Chunks have the following properties:
#-They are bounded planes composed of ordered sets of coordinates
#-Each chunk is of uniform dimensions in x, y and z axis
#-No two chunks can contain the same coordinate object
#-Active chunks receive ticks
#-Inactive chunks store the last game turn they were active
#-The chunk that contains a given coordinate can be determined mathematically
# by using integer division of the coordinate's (x,y,z) by the chunkSize 
class Chunk:
    def __init__(self, key, gameTurn, chunkSize = [16,16,1]):
        self.key = key
        self.XYZ = keyToXYZ(key)
        self.chunkSize = chunkSize
        self.gameTurnCreated = gameTurn
        self.coordinates = dict()
        self.coordinatesList = []
        self.chunkRange = self.defineChunkRange()
        self.makeCoordinates(self.chunkRange)
        self.lastActiveGameTurn = self.gameTurnCreated
    def defineChunkRange(self):
        x = self.XYZ[0] * 16
        y = self.XYZ[1] * 16
        z = self.XYZ[2] #* 16
        xRange = [ x, x + (self.chunkSize[0]-1)]
        yRange = [ y, y + (self.chunkSize[1]-1)]
        zRange = [ z, z + (self.chunkSize[2]-1)]
        return [xRange, yRange, zRange]
    def makeCoordinates(self, ranges):
        for x in range(ranges[0][0], (ranges[0][1] +1) ): 
            for y in range(ranges[1][0], (ranges[1][1] +1) ):
                for z in range(ranges[2][0], (ranges[2][1] +1) ): 
                    key = makeKey([x,y,z]) #Make a key string
                    #Make coordinate object and store it
                    c = Coordinate(key) 
                    self.coordinates[key] = c
                    self.coordinatesList.append(c)
    def TICK(self, TICK, gameTurn):
        self.lastActiveGameTurn = gameTurn
        for c in self.coordinatesList:
            c.TICK(TICK)
    def addElement(self, coordinateKey, element):
        self.coordinates[coordinateKey].addElement(element)
    #Return a boolean of whether element removed successfully
    def removeElement(self, coordinateKey, element):
        self.coordinates[coordinateKey].removeElement(element)
    def load(self):
        for c in self.coordinatesList:
            c.load()
    def unload(self):
        for c in self.coordinatesList:
            c.unload()