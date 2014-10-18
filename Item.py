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
#-'layer'       => Numeric value to be used in render ordering. 
class Item(Matter):
    def __init__(self, **kwargs):
        Matter.__init__(self, **kwargs)
        self.acceptedKWARGS = {'tall': 0, 'floatOffset': [0.5, 0.5], 'layer': 1.5}
        for key in self.acceptedKWARGS.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.acceptedKWARGS[key])
    def TICK(self, TICK):
        pass #Default items do nothing on Tick
    def determinePixelOffset(self):
        px = ( self.width/2.0) - self.floatOffset[0] * self.width
        py = (self.height/2.0) - self.floatOffset[1] * self.height
        py = py - element.tall - int(element.tall * element.floatOffset[1])
        self.pixelOffsets = [int(px), int(py)]