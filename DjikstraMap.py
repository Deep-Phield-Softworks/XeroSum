#!/usr/bin/env python
from AoE import *

class DjikstraMap:
    def __init__(self, shape, selectedKeys, setValue = [0, False, 0]):
        self.shape = shape
        self.selectedKeys = selectedKeys
        self.setValue = setValue
        #The coordinate keys are already in shape...
        self.keys    = self.shape.nDimensionalArray #Use shape's nD Key list
        #Create a dictionary to store the values
        self.MapVals = dict()
        #Populate the Map Values
        for x in range(0,len(self.keys)):
            for y in range(0,len(self.keys[x])):
                for z in range(0,len(self.keys[x][y])):
                    self.MapVals[self.keys[x][y][z]] = [10000, False, 0]
        for key in self.selectedKeys:
            if self.MapVals.has_key(key):
                self.MapVals[key] = setValue #Set the goals to low values
    def processMap(self):
        pass
    
    def findPath(self):
        nodes = []
        return nodes

    #Add together the values of two DMAPS
    def add(self, DMAP):
        pass
    #Subtract the values of two DMAPS
    def subtract(self, DMAP):
        pass