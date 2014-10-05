#!/usr/bin/env python
from unboundMethods import *
from Matter import Matter
from ImageManifests import SPRITE_MANIFEST

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
class Entity(Matter): #entity(world, coordinateKey, imageKey)
    def __init__(self,world, coordinateKey, imageKey, name = None, tall = 0, floatOffset = [0.5,0.5]):
        self.world = world
        self.imageKey =  imageKey 
        self.SpriteSheet = SPRITE_MANIFEST[self.imageKey] #SpriteSheet object that provides sprite frames
        self.width   = self.SpriteSheet.frameWidth
        self.height  = self.SpriteSheet.frameHeight
        Matter.__init__(self, imageKey, name, self.height, floatOffset)
        self.coordinateKey = coordinateKey
        self.lastFrame = 0 #the rendered last frame in a "strip" of frames
        self.facing = 5
        self.lastFacing = 5
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
        py = ( TILE_HEIGHT/2.0) + (self.floatOffset[1] * self.height)
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
        pass
        if self.path: #If path is not None
        #Check to see if enough time has accumulated to advance frames
            self.tickAccumulator += TICK
            if self.tickAccumulator >= self.frameThreshhold:
                self.tickAccumulator = 0
                if self.lastFrame < (len(self.animation)-1):
                    self.lastFrame += 1
                else:
                    self.lastFrame = 0
        ###Putting this in to "fix" "IndexError: list index out of range"###
            ###This may cause other problems, but seems to stop the exception###
            if len(self.animation) <= self.lastFrame:
                self.lastFrame = len(self.animation) - 1
            ###Putting this in to "fix" "IndexError: list index out of range"###
            ###This may cause other problems, but seems to stop the exception###
            self.toBlit = self.animation[self.lastFrame]
        else: #If no path use idle animation
            self.animation = self.SpriteSheet.animations[5]
            self.toBlit = self.animation[self.facing]
        if self.path: #If path is not None
            self.moveAccumulator += TICK #Add the ticks in
            if self.moveAccumulator >= self.moveThreshhold: #If enough ticks...
                self.moveAccumulator = 0 #Reset Accumulator
                more = self.path.advance()      #Advance the path to the next step
                if more:
                    next = self.path.nodes[self.path.stepIndex] #Lookup next node
                    self.facing = self.path.facings[self.path.stepIndex]
                    self.animation = self.SpriteSheet.animations[self.facing]
                    ######MOVE COORDINATES HERE############
                else:
                    self.path = None
                    self.animation = self.SpriteSheet.animations[5]