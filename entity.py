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
class Entity(Matter): #entity(world, coordinate_key, imageKey)
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
        self.sprite_sheet = sprite_manifest[self.image_key] 
        self.width   = self.sprite_sheet.frame_width
        self.height  = self.sprite_sheet.frame_height
        self.tall    = self.height
        self.last_frame = 0 #the rendered last frame in a "strip" of frames
        self.facing = 5
        self.animation = self.sprite_sheet.animations[self.facing]
        self.frame_threshold = 100 #167
        self.move_threshold  = 500
        self.tick_accumulator = 0
        self.move_accumulator = 0
        self.path = None
        self.to_blit = self.animation[self.last_frame]
        self.pixel_offsets = self.determine_pixel_offset()
        
    def determine_pixel_offset(self):
        px = (TILE_WIDTH/2.0)  - (self.float_offset[0] * self.width)
        py = (TILE_HEIGHT/2.0)
        py = py - self.tall #- int(self.tall * self.float_offset[1])
        #py = py - int(self.tall * self.float_offset[1])
        return plist([int(px), int(py)])
    def load(self):
        self.sprite_sheet = sprite_manifest[self.image_key]
        self.animation = self.sprite_sheet.animations[self.facing]
        self.to_blit = self.animation[self.last_frame]
    def unload(self):
        self.sprite_sheet = None
        self.animation = None
        self.to_blit = None
    def TICK(self, TICK):
        if self.path: #If path is not None
        #Check to see if enough time has accumulated to advance frames
            self.tick_accumulator += TICK
            if self.tick_accumulator >= self.frame_threshold:
                self.tick_accumulator = 0
                if self.last_frame < (len(self.animation)-1):
                    self.last_frame += 1
                else:
                    self.last_frame = 0
            if len(self.animation) <= self.last_frame:
                self.last_frame = len(self.animation) - 1
            self.to_blit = self.animation[self.last_frame]
        else: #If no path use idle animation
            self.animation = self.sprite_sheet.animations[5]
            self.to_blit = self.animation[self.facing]
        if self.path: #If path is not None
            self.move_accumulator += TICK #Add the ticks in
            if self.move_accumulator >= self.move_threshold: #If enough ticks...
                self.move_accumulator = 0 #Reset Accumulator
                lastKey = self.path.nodes[self.path.step_index]
                more = self.path.advance()      #Advance the path to the next step
                if more:
                    next_key = self.path.nodes[self.path.step_index] #Lookup next node
                    self.facing = self.path.facings[self.path.step_index]
                    self.animation = self.sprite_sheet.animations[self.facing]
                    self.coordinate_key = next_key
                    self.world.move_element(self, lastKey, next_key)
                else:
                    self.path = None
                    self.animation = self.sprite_sheet.animations[5]
