#!/usr/bin/env python
import pygame
from xeroConstants import *
#Figure class (a sprite manager class)
class figure:
    def __init__(self,  MAPX, MAPY, section, image, px, py, id, radius = 1):
        self.id = str(id) #An identifying string
        self.image = image #image object that provides sprite frames
        self.lastFrame = 0 #the rendered last frame in a "strip" of frames
        self.facing = 5
        self.lastFacing = 5
        self.animation = self.image.animations[self.facing]
        self.width   = self.image.frameWidth
        self.height  = self.image.frameHeight
        self.px = px
        self.py = py
        self.MAPX = MAPX
        self.MAPY = MAPY
        self.section = section
        self.back = None
        self.radius = radius
        self.frameThreshhold = 100#167
        self.moveThreshhold  = 500
        self.tickAccumulator = 0
        self.moveAccumulator = 0
        self.path = None
        
    #Set px, py position
    def setPos(self, px, py):
        self.px = px
        self.py = py
    
    #Set internal MAP position data
    def setMapPos(self, MAPX, MAPY):
        self.MAPX = MAPX
        self.MAPY = MAPY
    
    #Draw the subsurface animation frame from image.animate[index of lastFrame]
    #on the given surface at coordiantes (self.x,self.y)
    def render(self, TICK, surface):
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
            toBlit = self.animation[self.lastFrame]
            surface.blit(toBlit,(self.px,self.py))
        else: #If no path use idle animation
            self.animation = self.image.animations[5]
            toBlit = self.animation[self.facing]
            surface.blit(toBlit,(self.px,self.py))
    
    #General purpose move command.
    #
    def move(self, TICK, speed = 1):
        if self.path: #If path is not None
            self.moveAccumulator += TICK #Add the ticks in
            if self.moveAccumulator >= self.moveThreshhold: #If enough ticks...
                self.moveAccumulator = 0 #Reset Accumulator
                more = self.path.advance()      #Advance the path to the next step
                if more:
                    next = self.path.path[self.path.stepIndex] #Lookup next node
                    self.facing = self.path.facings[self.path.stepIndex]
                    self.animation = self.image.animations[self.facing]
                    self.section = next[0] #Set section to node's section
                    self.MAPX = next[1] #Adjust self.MAPX
                    self.MAPY = next[2] #Adjust self.MAPY
                else:
                    self.path = None
                    self.animation = self.image.animations[5]
        return [self.section, self.MAPX, self.MAPY]        
    
    def getBack(self, surface):
        self.rect = pygame.Rect((self.px, self.py), (self.width, self.height))
        self.back = pygame.Surface((self.width, self.height))
        self.back.blit(surface,ORIGIN,self.rect) #Store sprite background
    
    def renderBack(self, surface):
        self.rect = pygame.Rect((self.px, self.py), (self.width, self.height))
        if self.back == None: #First time rendering, create a background surface
            self.back = pygame.Surface((self.width, self.height))
            self.back.blit(surface,ORIGIN,self.rect) #Store sprite background
        else:
            #Not first time rendering, restore background to surface
            surface.blit(self.back,(self.px,self.py))
        surface.blit(self.back,(self.px,self.py))
    
