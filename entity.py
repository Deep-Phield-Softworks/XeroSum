#!/usr/bin/env python
from persistent.list import PersistentList as plist


from imagemanifests import sprite_manifest
from matter import Matter
from unboundmethods import TILE_WIDTH, TILE_HEIGHT 
#Entities are objects that are "alive". They can:
#-move themselves
#-be killed/destroyed
#-may pick and drop up items
#-may have an inventory
#-may use items
#-may interact with features
#-have a speed which defines how often they act
#-have an action queue that defines their actions and the time costs
#Examples: a dog, person
#Accepted **kwargs in self.accepted_kwargs:
#-'world' => World object that contains the entity and to whom it reports its
#            movements
#-'coordinate_key' => key string of containing Coordinate
#-'impassible'  => Boolean value for whether the Entity makes the containing
#                  Coordinate not be considered by Path objects. I left this as
#                  optional but defaults to True as I can imagine incorporeal or
#                  miniscule entities that might not block movement.
#-'float_offset' => list of two floats that represent how far from the center of
#                  the parent Coordinate the object lies. [0.5, 0.5] would be
#                  centered on the parent Coordinate.
#-'layer'       => Numeric value to be used in render ordering. 
class Entity(Matter): 
    def __init__(self, **kwargs):
        Matter.__init__(self, **kwargs)
        self.accepted_kwargs = {'world': None,
                                'coordinate_key': '0_0_0',
                                'impassible': True,
                                'layer': 1.2,
                                'float_offset': plist([0.5, 0.5])
                                               }
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key]) 
        #Render related local variables..
        self.width   = sprite_manifest[self.image_key].frame_width
        self.height  = sprite_manifest[self.image_key].frame_height
        self.tall    = self.height
        self.frame = 0 #the rendered last frame in a "strip" of frames
        self.facing = 5
        #Thresholds for changes in milliseconds
        self.frame_threshold = 100 
        self.move_threshold  = 500
        self.tick_accumulator = 0
        self.move_accumulator = 0
        self.path = None
        self.pixel_offsets = self.determine_pixel_offset()
        
    def determine_pixel_offset(self):
        px = (TILE_WIDTH/2.0)  - (self.float_offset[0] * self.width)
        py = (TILE_HEIGHT/2.0)
        py = py - self.tall
        return plist([int(px), int(py)])
    
    def to_blit(self):
        return sprite_manifest[self.image_key].animations[self.facing][self.frame]
    
    def tick(self, TICK):
        self.tick_move(TICK)
        self.tick_animation(TICK)
        
    def tick_move(self, TICK):
        self.move_accumulator += TICK #Add the ticks in
        if self.move_accumulator >= self.move_threshold: #If enough ticks...
            self.move_accumulator = 0 #Reset Accumulator
            key = self.path.nodes[self.path.step_index]
            next = self.path.advance() 
            if next:
                self.facing = self.path.facings[self.path.step_index]
                self.world.move_element(self, key, next)
            else:
                self.path = None
                self.frame = 5
    
    def tick_animation(self, TICK):
        strip = sprite_manifest[self.image_key].animations[self.facing]
        if self.path: #If path is not None
        #Check to see if enough time has accumulated to advance frames
            self.tick_accumulator += TICK
            if self.tick_accumulator >= self.frame_threshold:
                self.tick_accumulator = 0
                if self.frame < (len(strip)-1):
                    self.frame += 1
                else:
                    self.frame = 0
            #if len(strip) <= self.frame:
            #    self.frame = len(strip) - 1