#!/usr/bin/env python
from Matter import Matter
#Tile objects are the ground.
#Tile objects are: 
#-immobile
#-cannot usually be destroyed
#-may affect travel speed through their coordinate
#-drawn first
#Examples: dirt floor, rubble floor, gravel floor
class Tile(Matter):
    def __init__(self, imageKey, name = None, tall = 0, speedModifier = None):
        Matter.__init__(self, imageKey, name, tall)
        self.speedModifier = speedModifier
        self.floatOffset = [0.0,0.0] #Tiles should not be offset. Would create gaps
    def determinePixelOffset(self):
        pass
    def TICK(self, TICK):
        pass