#!/usr/bin/env python
#Generic entity object class
import pygame

class SpriteSheet:
    #Constructor
    def __init__(self, imageKey, spriteDir, framesWide, framesHigh, COLORKEY = pygame.Color('#0080ff') ): 
        self.imageKey = imageKey   #Image file name
        self.imagepath = spriteDir + imageKey
        self.surface = pygame.image.load(self.imagepath).convert()
        self.surface.set_colorkey(COLORKEY)
        self.framesWide = framesWide #How many animation frames wide is image
        self.framesHigh = framesHigh #How many animation frames high is image
        self.pixelsWide = self.surface.get_width() #How many pixels wide is image
        self.pixelsHigh = self.surface.get_height() #How many pixels high is image
        self.frameWidth  = self.pixelsWide/self.framesWide#One frame's width
        self.frameHeight = self.pixelsHigh/self.framesHigh#One frame's height
        #Create an empty list for the animation "strips"
        self.animations = []
        self.populateAnimations() #Create the animation "strips"
        
    
    #Create animation as a set of pygame subsurfaces. Store these as a nested
    #list for easy iteration through individual "frames".
    #I am leaving a hook for different sprite sheet layouts as arguement pattern
    def populateAnimations(self, pattern = None):
        #Default Sprite Sheet Pattern
        
        for x in range(10): #Create 10 empty "animation slots"
            self.animations.append([])
        #Populate Slot 0 (IDK What to put here atm)
        self.animations[0] = self.createIdleStrip() #!!PLACEHOLDER!!#
        
        #Populate Slot 1 (Walking SW)
        self.animations[1] = self.createStrip(1)
        
        #Populate Slot 2 (Walking S)
        self.animations[2] = self.createStrip(1)
        
        #Populate Slot 3 (Walking SE)
        self.animations[3] = self.createStrip(1)
        
        #Populate Slot 4 (Walking W)
        self.animations[4] = self.createStrip(3)
        
        #Populate Slot 5 (Standing Still Facing in All 9)
        self.animations[5] = self.createIdleStrip() #!!PLACEHOLDER!!#
        
        #Populate Slot 6 (Walking E)
        self.animations[6] = self.createStrip(2)
        
        #Populate Slot 7 (Walking NW)
        self.animations[7] = self.createStrip(0)
        
        #Populate Slot 8 (Walking N)
        self.animations[8] = self.createStrip(0)
        
        #Populate Slot 9 (Walking NE)
        self.animations[9] = self.createStrip(0)
    
    #Split a strip into a temp array of ordered subsurfaces
    #for assignment in proper "animation order"
    def createStrip(self, row):
        #Derive top or uppermost y coordinate by dividing
        #pixel height by total frame rows. Then multiply that by row.
        #Ex. Row 0 top would always be 0. For a 256x256 pixel w/ 4 rows:
        #Row 3 would be (256/4)= 64, 64*3 = 192.
        width  = self.frameWidth
        height = self.frameHeight
        top =  height * row
        left = 0 #Initially left has an x axis value of 0.
        strip = []
        #The bottom rows follow different rules than top rows
        if row > 1:
            for x in range(self.framesWide): #For each frame in the strip
                Rect = pygame.Rect((left, top), (width, height))
                frame = self.surface.subsurface(Rect)
                strip.append(frame)
                left += width #Add width for each
        else:  #If the row is one of the top two with less frames...
            #There are 5 frames in the top two rows
            #These frames are for moving south and north
            for x in range(5): #For each frame in the strip
                Rect = pygame.Rect((left, top), (width, height))
                frame = self.surface.subsurface(Rect)
                strip.append(frame)
                left += width #Add width for each
            #The basic 5 frames are split and appended.
            #To complete the cycle, loop back through
            for x in range(3,0,-1):
                strip.append(strip[x])
        return strip
    
    def createIdleStrip(self):
        strip0 = self.createStrip(0)
        strip1 = self.createStrip(1)
        strip2 = self.createStrip(2)
        strip3 = self.createStrip(3)
        strip = []
        north = strip0[2]
        south = strip1[2]
        east  = strip2[4]
        west  = strip3[4]
        ##Populate Slot 0 (Facing S) #Placeholder
        strip.append(south)
        ##Populate Slot 1 (Facing SW)
        strip.append(south)
        ##Populate Slot 2 (Facing S)
        strip.append(south)
        ##Populate Slot 3 (Facing SE)
        strip.append(south)
        ##Populate Slot 4 (Facing W)
        strip.append(west)
        ##Populate Slot 5 (Facing S)#Placeholder/Initial
        strip.append(south)
        ##Populate Slot 6 (Facing E)
        strip.append(east)
        ##Populate Slot 7 (Facing NW)
        strip.append(north)
        ##Populate Slot 8 (Facing N)
        strip.append(north)
        ##Populate Slot 9 (Facing NE)
        strip.append(north)
        return strip
