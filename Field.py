#!/usr/bin/env python
from AoE import *
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
#
#Accepted **kwargs in self.acceptedKWARGS:
#-'name'   => either a string or None
#-'origin' => key string of a Coordinate object that represents the "center" of
#             a Field
#-'AoEshape' => Shape or Shape subclass that defines the area that the field
#               encompasses
class Field:
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        
    def __init__(self, **kwargs):
        #origin, AoEShape, magnitude, name = None
        self.acceptedKWARGS = {'name': None,
                               'origin': '0_0_0',
                               'AoEshape': Shape(**kwargs),
                               'layer': 0.0}
        for key in self.acceptedKWARGS.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.acceptedKWARGS[key]) 
    def TICK(self, TICK):
        errorString = "Subclass of Field must implement TICK method"
        raise NotImplementedError(errorString)