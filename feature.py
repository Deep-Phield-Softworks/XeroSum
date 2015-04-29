#!/usr/bin/env python
from persistent.list import PersistentList as plist


from matter import Matter
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
#-'float_offset' => list of two floats that represent how far from the center of
#                  the parent Coordinate the object lies. [0.5, 0.5] would be
#                  centered on the parent Coordinate.
#-speed_modifier => float value in range 0 < x < float(+inf). Represents the
#                  change in travel speed caused by this tile. Lower values are
#                  faster.
#-'impassible'  => Boolean value for whether the feature makes the containing
#                  Coordinate not be considered by Path objects 
#-'blocksLOS'   => Boolean value for whether the feature makes the containing
#                  Coordinate block Line of Sight
#-'layer'       => Numeric value to be used in render ordering.
#-'float_offset_ranges' => Tuples of floats for range of float Offsets
class Feature(Matter):
    def __init__(self, **kwargs):
        Matter.__init__(self, **kwargs)
        self.accepted_kwargs = {'tall': 0,
                                                  'float_offset': plist([0.5, 0.5]),
                                                  'float_offset_ranges': plist(((0.25, 0.75),(0.25, 0.75))),
                                                  'speed_modifier': 1.0,
                                                  'layer': 1.0,
                                                  'impassible': False,
                                                  'blocksLOS': False 
                                                }
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key])
        self.pixel_offsets = self.determine_pixel_offset()
    
    def determine_pixel_offset(self):
        px = ( self.width/2.0) - self.float_offset[0] * self.width
        py = (self.height/2.0) - self.float_offset[1] * self.height
        py = py - self.tall - int(self.tall * self.float_offset[1])
        self.pixel_offsets = plist([int(px), int(py)])
    
    def tick(self, TICK):
        pass    
