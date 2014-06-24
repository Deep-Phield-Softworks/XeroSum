#!/usr/bin/env python
from tile import tile
from random import randint

#This makes a level map using the tile objects to store each xyz coordinate.
#Be sure to call makeBaseLayer() before blitting map the first time
class section:
                  #xMax = 800, yMax = 600,
    def __init__(self, name, (Xoffset, Yoffset) = (0,0), tileSize = 64, baseTerrainImage = 'grass.png'):
        self.name = name
        self.base = baseTerrainImage
        self.Xoffset = Xoffset
        self.Yoffset = Yoffset
        self.tileSize = tileSize
        self.MAP = []
        self.spool = []
        self.MAP_WIDTH   = 16
        self.MAP_HEIGHT  = 16
        self.TILE_WIDTH  = int(self.tileSize)
        self.TILE_HEIGHT = int(self.tileSize/2)
        #Create empty MAP data structure.
        for x in range (self.MAP_WIDTH):
            self.MAP.append([])
            for y in range (self.MAP_HEIGHT):
                self.MAP[x].append([])
        #Create an empty list for dirty tiles
        self.dirty = []
    
    #Render all the dirty tiles. Now the list of dirty tiles should be clear.
    def render(self, TICK, surface):
        for tile in self.dirty:
            tile.render(TICK, surface)
        self.dirty = []
    #Method to dirty all tiles when loading new sectors.
    def dirtyAll(self):
        for MAPX in range (self.MAP_WIDTH):
            for MAPY in range (self.MAP_HEIGHT):
                for tile in self.MAP[MAPX][MAPY]:
                    self.dirty.append(tile)
                
    #This makes a bottom layer of terrain using the image file in base.
    def makeBaseLayer(self):
        #Fill MAP[x..][y..][z == 0] with Base tile         
        for MAPX in range (self.MAP_WIDTH):
            for MAPY in range (self.MAP_HEIGHT):
                px = (MAPX - MAPY) * (self.TILE_WIDTH  / 2 ) + self.Xoffset
                py = (MAPX + MAPY) * (self.TILE_HEIGHT / 2 ) + self.Yoffset
                self.MAP[MAPX][MAPY].append([])
                self.MAP[MAPX][MAPY][0] = tile(px,py, self.base, MAPX , MAPY, 0)
    
    #Adjust each tile tile's pixel (x,y) 
    def offsetTiles (self, (offsetX, offsetY)):
        for x in range (self.MAP_WIDTH):
            for y in range (self.MAP_HEIGHT):
                for z in self.MAP[x][y]:
                    if isinstance(z, tile):
                        z.px = z.basePX + offsetX #Confused yet?
                        z.py = z.basePY + offsetY
    #Given:Click as (x,y)
    #Determine if the click is within the bounds of the section.
    def withinSection(self, click):
        width = self.TILE_WIDTH
        height = self.TILE_HEIGHT
        bool = False
        # A is at the 9 O'clock Position. The rest go counter-clockwise.
        A, B, C, D = [0,0],[0,0],[0,0],[0,0]
        A[0] = self.MAP[0][-1][0].px
        A[1] = self.MAP[0][-1][0].py + (height/2)
        B[0] = self.MAP[-1][-1][0].px + (width/2)
        B[1] = self.MAP[-1][-1][0].py + height
        C[0] = self.MAP[-1][0][0].px + width
        C[1] = self.MAP[-1][0][0].py + (height/2)
        D[0] = self.MAP[0][0][0].px + (width/2)
        D[1] = self.MAP[0][0][0].py
        
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

    #Function to place a type of Random terrain features. MUST be called after
    #makeBaseLayer() has been called.
    #Parameters:
    #-chance == chance to place as 1 in chance, ex: chance == 4 -> 1 in 4
    #-passable == whether terrain feature blocks movement through map square
    #-tall == whether feature is taller than 32 pixels
    def randomLayer(self, image, chance, conceals = True, tall = False, tallMod = 32):
        for MAPX in range (self.MAP_WIDTH):
            for MAPY in range (self.MAP_HEIGHT):
                roll = randint(1, chance)
                if roll == 1:
                    px = (MAPX - MAPY) * (self.TILE_WIDTH  / 2 ) + self.Xoffset
                    py = (MAPX + MAPY) * (self.TILE_HEIGHT / 2 ) + self.Yoffset
                    #If feature is taller than the normal 32 pixels...
                    if tall: #Move top left of image Rect By tallMod
                        py = py - tallMod  #tallMod == 32 by default
                    #This basically means add terrain feature to MAP[x][y][z]
                    MAPZ = len(self.MAP[MAPX][MAPY])
                    t = tile(px, py, image, MAPX, MAPY, MAPZ, conceals, tall)
                    self.MAP[MAPX][MAPY].append(t)
    
    #Create a flat list of tiles.
    def spoolTiles(self):
        for MAPY in range (self.MAP_HEIGHT):
            for MAPX in range (self.MAP_WIDTH):
                self.spool.append(self.MAP[MAPX][MAPY][0])
    
    def loadImages(self, tileManifest):
        for MAPX in range (self.MAP_WIDTH):
            for MAPY in range (self.MAP_HEIGHT):
                for tile in self.MAP[MAPX][MAPY]:
                    tile.loadImage(tileManifest)
    
    def unloadImages(self):
        for MAPX in range (self.MAP_WIDTH):
            for MAPY in range (self.MAP_HEIGHT):
                for tile in self.MAP[MAPX][MAPY]:
                    tile.unloadImage()