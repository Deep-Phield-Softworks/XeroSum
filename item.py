#!/usr/bin/env python
from persistent.list import PersistentList as plist


from matter import Matter
from manifests import item_manifest
from manifests import fx_manifest 

#Items are objects that can be placed into inventory. They are:
#-unable to move themselves(usually)
#-movable from ground to inventory
#-may be usable
#-may be consumable
#Example: gun or loaf of bread
#
#Accepted **kwargs in self.accepted_kwargs:
#-'tall' => int number of pixels. For an object that is taller than normal and
#           must have its drawn position offset to be drawn properly.
#-'floatOffset' => list of two floats that represent how far from the center of
#                  the parent Coordinate the object lies. [0.5, 0.5] would be
#                  centered on the parent Coordinate.
#-'layer'    => Numeric value to be used in render ordering.
#-'frame'  =>  Tuple describing frame position in the ItemSheet referenced by item_manifest['image_key']
#-'weight' => Float value describing the weight of the item
#-'use_sound' => Value points to the .ogg file of the sound the item makes on use. Default for now is explosion

class Item(Matter):
    def __init__(self, **kwargs):
        Matter.__init__(self, **kwargs)
        self.accepted_kwargs = {'tall': 0, 'float_offset': plist([0.5, 0.5]), 'layer': 1.5,
                                'frame': (0, 0), 'weight' : 0.0, 'use_sound' : 'explosion.ogg'}
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key])
    
    def to_blit(self):
        return item_manifest[self.image_key].frames[self.frame[0]][self.frame[1]]
    
    def tick(self, TICK):
        pass #Default items do nothing on Tick
    
    def determine_pixel_offset(self):
        px = ( self.width/2.0) - self.float_offset[0] * self.width
        py = (self.height/2.0) - self.float_offset[1] * self.height
        py = py - element.tall - int(element.tall * element.float_offset[1])
        self.pixel_offsets = [int(px), int(py)] 
