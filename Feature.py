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
class Feature(Matter):
    def __init__(self, imageKey, name = None, speedModifier = 1.0, tall = 0, floatOffset = [0.5,0.5], impassible = False, blocksLOS = False):
        Matter.__init__(self, imageKey, name)
        self.tall        = tall
        self.floatOffset = floatOffset
        self.impassible  = impassible
        self.blocksLOS   = blocksLOS
        self.height = TILE_MANIFEST[self.imageKey].get_height()
        self.width  = TILE_MANIFEST[self.imageKey].get_width()
        self.pixelOffsets = self.determinePixelOffset()
    def determinePixelOffset(self):
        px = ( self.width/2.0) - self.floatOffset[0] * self.width
        py = (self.height/2.0) - self.floatOffset[1] * self.height
        self.pixelOffsets = [int(px), int(py)]
    def TICK(self, TICK):
        pass    