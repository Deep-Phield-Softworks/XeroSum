#!/usr/bin/env python
from Matter import Matter
from ImageManifests import TILE_MANIFEST

#Feature objects are facets of the world that are:
#-unable to move themselves(usually)
#-cannot be picked up or carried
#-can act and be acted upon
#-may change states over time
#-destructible
#-may block travel through their coordinate
#-may block dropping items into their coordinate
#Examples would be a chest, door and a tree
#
#Accepted **kwargs in self.acceptedKWARGS:
#-'tall' => int number of pixels. For an object that is taller than normal and
#           must have its drawn position offset to be drawn properly.
#-'floatOffset' => list of two floats that represent how far from the center of
#                  the parent Coordinate the object lies. [0.5, 0.5] would be
#                  centered on the parent Coordinate.
#-speedModifier => float value in range 0 < x < float(+inf). Represents the
#                  change in travel speed caused by this tile. Lower values are
#                  faster.
#-'impassible'  => Boolean value for whether the feature makes the containing
#                  Coordinate not be considered by Path objects 
#-'blocksLOS'   => Boolean value for whether the feature makes the containing
#                  Coordinate block Line of Sight
#-'layer'       => Numeric value to be used in render ordering.
#-'floatOffsetRanges' => Tuples of floats for range of float Offsets
class Feature(Matter):
    def __init__(self, **kwargs):
        Matter.__init__(self, **kwargs)
        self.acceptedKWARGS = {'tall': 0,
                               'floatOffset': [0.5, 0.5],
                               'floatOffsetRanges': ((0.25, 0.75),(0.25, 0.75)),
                               'speedModifier': 1.0,
                               'layer': 1.0,
                               'impassible': False,
                               'blocksLOS': False }
        for key in self.acceptedKWARGS.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.acceptedKWARGS[key])
        self.height = TILE_MANIFEST[self.imageKey].get_height()
        self.width  = TILE_MANIFEST[self.imageKey].get_width()
        self.pixelOffsets = self.determinePixelOffset()
    def determinePixelOffset(self):
        px = ( self.width/2.0) - self.floatOffset[0] * self.width
        py = (self.height/2.0) - self.floatOffset[1] * self.height
        self.pixelOffsets = [int(px), int(py)]
    def TICK(self, TICK):
        pass    