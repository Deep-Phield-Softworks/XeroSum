#!/usr/bin/env python
import pygame
import libraryXero as lib


class tile:
    #Initialize the tile.
    def __init__(self, px , py , imagename, mapX, mapY, mapZ, conceals = False, tall = False ):
        self.px = px
        self.py = py
        self.basePX = px
        self.basePY = py
        self.w = 32
        self.h = 32
        self.imagename = imagename
        self.conceals = conceals
        self.image = None #self.image = pygame.image.load(self.imagename).convert_alpha()
        self.MAPX = mapX
        self.MAPY = mapY
        self.MAPZ = mapZ
        self.tall = tall
    
    #Tell tile to render itself to a surface
    def render(self, TICK, surface):
        surface.blit(self.image,(self.px,self.py))
    
    #Given: (x,y) of a mouse click
    #Determine if the click is within a tile
    def withinTile(self,click, width = 64, height = 32):
        bool = False
        x = self.px
        y = self.py
        #4 points that define the rhombus
        A = (x,(y + (height/2)) )           #9 O'clock
        B = ((x + (width/2)),(y + height))  #6 O'clock
        C = ((x + width),(y + (height/2))) #3 O'clock
        D = ((x + (width/2)),y)             #12 O'clock 
    
        if (self.leftOf(A,D,click) > 0):
            if (self.leftOf(B,C,click) < 0):
                if (self.leftOf(D,C,click) > 0):
                    if (self.leftOf(A,B,click) < 0):
                        bool = True
        return bool
    
    #Given: 2 points that for a line segment and a third point
    #Determine if the third point is:
    #-"left and/or above" the line (returns a positive integer),
    #-"on the line" (returns 0), or
    #-"right and/or below" the line (returns a negative integer)
    def leftOf(self, one, two, point):
        X1 = one[0]
        X2 = two[0]
        Y1 = one[1]
        Y2 = two[1]
        Px = point[0]
        Py = point[1]
        left = (X2 - X1)*(Py - Y1) - (Y2 - Y1)*(Px - X1)
        return left

    
    #Use a tile's instance variables to return its XYZ coordinates.
    def tileMapID(self):  
        ID = [None,None,None] #Make empty list
        ID[0] = self.MAPX
        ID[1] = self.MAPY
        ID[2] = self.MAPZ
        return ID
        
    #Load the image file before the MAP object is first rendered
    def loadImage(self, tileManifest):
        self.image = tileManifest[self.imagename]
    
    #Clear the self.image variable so that the object can be pickled.
    def unloadImage(self):
        self.image = None
    
    #Check to make sure that this tile can be entered
    def passable(self):
        return self.passable
    #This defines what to do if the
    def on_step(self):
        pass
    #This is SO hacked together but will have to do for now.
    #It pulls the first half of the image name as the tile's name.
    #So bush.png becomes "bush"
    def name(self):
        split = self.imagename.split(".")
        name = split[0]
        return name