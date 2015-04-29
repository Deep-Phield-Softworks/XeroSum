#!/usr/bin/env python
from aoe import *

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
#-'aoe_shape' => Shape or Shape subclass that defines the area that the field
#               encompasses
class Field:
    def __init__(self, **kwargs):
        self.accepted_kwargs = {'name': None,
                                                 'origin': '0_0_0',
                                                 'aoe_shape': Shape(**kwargs),
                                                 'pixel_offsets': [0,0],
                                                 'layer': 0.0
                                                }
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key]) 
    
    def tick(self, TICK):
        error_string = "Subclass of Field must implement tick method"
        raise NotImplementedError(error_string)
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
