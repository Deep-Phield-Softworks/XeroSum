#!/usr/bin/env python
from matter import Matter
#Tile objects are the ground.
#Tile objects are: 
#-immobile
#-cannot usually be destroyed
#-may affect travel speed through their coordinate
#-drawn first
#-should have a float offset of [0.0,0.0] to prevent gaps.
#Examples: dirt floor, rubble floor, gravel floor
#
#Accepted **kwargs in self.acceptedKWARGS:
#-speedModifier => float value in range 0 < x < float(+inf). Represents the
#                  change in travel speed caused by this tile. Lower values are
#                  faster.
#-'layer'       => Numeric value to be used in render ordering. 
class Tile(Matter):
    def __init__(self, **kwargs):
        Matter.__init__(self, **kwargs)
        self.acceptedKWARGS = {'speedModifier': 1.0, 'layer': 0.1}
        for key in self.acceptedKWARGS.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.acceptedKWARGS[key])
        #No Tiles offset. Would create gaps. Only here as placeholder values.
        self.floatOffset = [0.0,0.0]
        self.pixelOffsets = [0, 0]
    def determinePixelOffset(self):
        #Tiles should not be offset. Would create gaps
        return self.pixelOffsets
    def TICK(self, TICK): 
        pass #Tiles do nothing by default when ticked atm.
    
