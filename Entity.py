#!/usr/bin/env python
from unboundMethods import *
from ImageManifests import SPRITE_MANIFEST
from Matter import Matter

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
#Accepted **kwargs in self.acceptedKWARGS:
#-'world' => World object that contains the entity and to whom it reports its
#            movements
#-'coordinateKey' => key string of containing Coordinate
#-'impassible'  => Boolean value for whether the Entity makes the containing
#                  Coordinate not be considered by Path objects. I left this as
#                  optional but defaults to True as I can imagine incorporeal or
#                  miniscule entities that might not block movement.
#-'floatOffset' => list of two floats that represent how far from the center of
#                  the parent Coordinate the object lies. [0.5, 0.5] would be
#                  centered on the parent Coordinate.
#-'layer'       => Numeric value to be used in render ordering. 
class Entity(Matter): #entity(world, coordinateKey, imageKey)
    def __init__(self, **kwargs):
        Matter.__init__(self, **kwargs)
        self.acceptedKWARGS = {'world': None,
                               'coordinateKey': '0_0_0',
                               'impassible': True,
                               'layer': 1.2,
                               'floatOffset': [0.5, 0.5]}
        for key in self.acceptedKWARGS.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.acceptedKWARGS[key]) 
        #Render related local variables..
        self.SpriteSheet = SPRITE_MANIFEST[self.imageKey] 
        self.width   = self.SpriteSheet.frameWidth
        self.height  = self.SpriteSheet.frameHeight
        self.tall    = self.height
        self.lastFrame = 0 #the rendered last frame in a "strip" of frames
        self.facing = 5
        self.animation = self.SpriteSheet.animations[self.facing]
        self.frameThreshhold = 100 #167
        self.moveThreshhold  = 500
        self.tickAccumulator = 0
        self.moveAccumulator = 0
        self.path = None
        self.toBlit = self.animation[self.lastFrame]
        self.pixelOffsets = self.determinePixelOffset()
        
    def determinePixelOffset(self):
        px = ( TILE_WIDTH/2.0)  - (self.floatOffset[0] * self.width)
        py = ( TILE_HEIGHT/2.0)
        py = py - self.tall #- int(self.tall * self.floatOffset[1])
        #py = py - int(self.tall * self.floatOffset[1])
        return [int(px), int(py)]
    def load(self):
        self.SpriteSheet = SPRITE_MANIFEST[self.imageKey]
        self.animation = self.SpriteSheet.animations[self.facing]
        self.toBlit = self.animation[self.lastFrame]
    def unload(self):
        self.SpriteSheet = None
        self.animation = None
        self.toBlit = None
    def TICK(self, TICK):
        if self.path: #If path is not None
        #Check to see if enough time has accumulated to advance frames
            self.tickAccumulator += TICK
            if self.tickAccumulator >= self.frameThreshhold:
                self.tickAccumulator = 0
                if self.lastFrame < (len(self.animation)-1):
                    self.lastFrame += 1
                else:
                    self.lastFrame = 0
            if len(self.animation) <= self.lastFrame:
                self.lastFrame = len(self.animation) - 1
            self.toBlit = self.animation[self.lastFrame]
        else: #If no path use idle animation
            self.animation = self.SpriteSheet.animations[5]
            self.toBlit = self.animation[self.facing]
        if self.path: #If path is not None
            self.moveAccumulator += TICK #Add the ticks in
            if self.moveAccumulator >= self.moveThreshhold: #If enough ticks...
                self.moveAccumulator = 0 #Reset Accumulator
                lastKey = self.path.nodes[self.path.stepIndex]
                more = self.path.advance()      #Advance the path to the next step
                if more:
                    nextKey = self.path.nodes[self.path.stepIndex] #Lookup next node
                    self.facing = self.path.facings[self.path.stepIndex]
                    self.animation = self.SpriteSheet.animations[self.facing]
                    self.coordinateKey = nextKey
                    self.world.moveElement(self, lastKey, nextKey)
                else:
                    self.path = None
                    self.animation = self.SpriteSheet.animations[5]