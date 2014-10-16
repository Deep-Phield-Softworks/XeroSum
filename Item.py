#!/usr/bin/env python
from Matter import Matter
#Items are objects that can be placed into inventory. They are:
#-unable to move themselves(usually)
#-movable from ground to inventory
#-may be usable
#-may be consumable
#Example: gun or loaf of bread
#
#Accepted **kwargs in self.acceptedKWARGS:
#-'tall' => int number of pixels. For an object that is taller than normal and
#           must have its drawn position offset to be drawn properly.
#-'floatOffset' => list of two floats that represent how far from the center of
#                  the parent Coordinate the object lies. [0.5, 0.5] would be
#                  centered on the parent Coordinate. 
class Item(Matter):
    def __init__(self, **kwargs):
        Matter.__init__(self, **kwargs)
        self.acceptedKWARGS = {'tall': 0, 'floatOffset': [0.5, 0.5], 'layer': 0}
        for key in self.acceptedKWARGS.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.acceptedKWARGS[key])
    def TICK(self, TICK):
        pass #Default items do nothing on Tick
    def determinePixelOffset(self):
        pass