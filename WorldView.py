#!/usr/bin/env python
import pygame, time, datetime
from unboundMethods import *
from ImageManifests import *
from Chunk import Chunk
from Tile import Tile
from Feature import Feature
from Item import Item
from Entity import Entity
from Field import Field
#worldView is a field object to render a portion of the world.
#Given:
#-origin as a coordinate object
#-magnitude
#Return: a worldView object which:
#-world view has a shape(cube) 
#-has its own pygame surface object
#-has a render method to draw on its surface
class WorldView:
    def __init__(self, world, origin, shape, SCREEN_SIZE):
        self.world       = world
        #First determine the shape and area of view
        self.origin      = origin
        self.shape       = shape
        self.areaKeyList = self.shape.areaKeyList
        self.nD          = self.shape.nDimensionalArray
        self.prepareChunks() #Determine chunks needed and have world load them
        for x in range(len(self.nD)):
            for y in range(len(self.nD[x])) :
                for z in range(len(self.nD[x][y])):
                    cKey = self.nD[x][y][z]
                    c = self.world.active[findParent(cKey)].coordinates[cKey]
                    self.nD[x][y][z] = c
        #Next initialize render variables
        self.SCREEN_SIZE = SCREEN_SIZE
        self.surface     = pygame.Surface(SCREEN_SIZE) #Surface((width, height))
        self.hitBoxList  = []
    def prepareChunks(self):
        #Generate a list of chunks to activate
        chunks = [] #Theoretically this will be a shorter list than world.active
        #For each coordinate key in self.area
        for coordKey in self.areaKeyList:
            XYZ = keyToXYZ(coordKey)
            #determine coordinates parent chunk
            parentChunk = findParent(coordKey)
            #check if chunk key is in the list...
            if parentChunk not in chunks: #If not...
                chunks.append(parentChunk)  #Add it...
        for parentChunk in chunks:    
            self.world.activateChunk(parentChunk)
    def render(self):
        self.hitBoxList = [] #Empty hitBoxList
        halfTileWide = int(TILE_WIDTH  / 2 ) #imported from unboundMethods
        halfTileHigh = int(TILE_HEIGHT / 2 ) #imported from unboundMethods
        xRange = range(len(self.nD))
        yRange = range(len(self.nD[0]))    
        #Render Tiles
        for y in yRange:
            for x in xRange:
                for z in range(len(self.nD[x][y])):
                    c = self.nD[x][y][z]
                    if not c.empty:
                        basepx = (x - y) * halfTileWide + PXOFFSET
                        basepy = (x + y) * halfTileHigh + PYOFFSET
                        for t in c.tiles:
                            px, py = basepx, (basepy - t.tall)
                            img = TILE_MANIFEST[t.imageKey]
                            self.surface.blit(img, (px, py))
                            rect = Rect( (px,py), (img.get_width(),img.get_height() ) )
                            self.hitBoxList.append([rect, t])
        #Render everything else
        for y in yRange:
            for x in xRange:
                for z in range(len(self.nD[x][y])):
                        c = self.nD[x][y][z]
                        if not c.empty:
                            basepx = (x - y) * halfTileWide + PXOFFSET
                            basepy = (x + y) * halfTileHigh + PYOFFSET
                            contents = c.contains()
                            for archtype in contents[1:]:
                                for element in archtype:
                                    if isinstance(element, Entity):
                                        img = element.toBlit
                                    else:
                                        img = TILE_MANIFEST[element.imageKey]
                                    px = basepx + element.pixelOffsets[0]
                                    py = basepy + element.pixelOffsets[1]- element.tall - int(element.tall * element.floatOffset[1])
                                    rect = Rect( (px,py), (img.get_width(),img.get_height() ) )
                                    self.hitBoxList.append([rect, element])
                                    self.surface.blit(img, (px, py))