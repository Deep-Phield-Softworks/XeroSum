#!/usr/bin/env python

#Field objects are effects or facets of the environment that:
#-can be considered to have an origin point
#-can "radiate" from their origin
#-have an area they encompass
#-can have varying magnitudes or values at different coordinates they encompass
#-may affect the coordinates they encompass
#-cannot be picked up or dropped directly
#-may be blocked by other objects
#-has a set of rules to define the shape of the area it encompasses
#-may have either a finite or infinite duration 
#Examples: a river, light from a torch, a heal spell, an attack from a gun
class Field:
    def __init__(self, origin, AoEShape, magnitude, name = None):
        self.origin     = origin
        self.AoEshape   = AoEShape
        self.magnitude  = magnitude
        self.name       = name
    def TICK(self, TICK):
        pass