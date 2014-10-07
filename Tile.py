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
    def __init__(self, imageKey, speedModifier = 1.0):
        Matter.__init__(self, imageKey)
        self.speedModifier = speedModifier
        self.floatOffset = [0.0,0.0]#No Tiles offset. Would create gaps
    def determinePixelOffset(self):
        pass #Tiles should not be offset. Would create gaps
    def TICK(self, TICK): 
        pass #Tiles do nothing by default when ticked atm