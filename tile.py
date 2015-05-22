#!/usr/bin/env python
from persistent.list import PersistentList as plist


from matter import Matter
from manifests import tile_manifest

#Tile objects are the ground.
#Tile objects are: 
#-immobile
#-cannot usually be destroyed
#-may affect travel speed through their coordinate
#-drawn first
#-should have a float offset of [0.0,0.0] to prevent gaps.
#Examples: dirt floor, rubble floor, gravel floor
#
#Accepted **kwargs in self.accepted_kwargs:
#-speedModifier => float value in range 0 < x < float(+inf). Represents the
#                  change in travel speed caused by this tile. Lower values are
#                  faster.
#-'layer'       => Numeric value to be used in render ordering. 
class Tile(Matter):
    def __init__(self, **kwargs):
        Matter.__init__(self, **kwargs)
        self.accepted_kwargs = {'speedModifier': 1.0, 'layer': 0.1, 'pathable': True}
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key])
        #No Tiles offset. Would create gaps. Only here as placeholder values.
        self.float_offset = plist([0.0,0.0])
        self.pixel_offsets = plist([0, 0])
    
    def to_blit(self):
        return tile_manifest[self.image_key]
    
    def determine_pixel_offset(self):
        #Tiles should not be offset. Would create gaps
        return self.pixel_offsets
    
    def tick(self, TICK): 
        pass #Tiles do nothing by default when ticked atm.
    
