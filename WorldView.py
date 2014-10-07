#!/usr/bin/env python
import pygame
from unboundMethods import *
from ImageManifests import *
from Tile import Tile
from Feature import Feature
from Item import Item
from Entity import Entity
from Field import Field
#worldView is an object made to render a portion of the world.
#Given:
#-world object
#-shape object
#-SCREEN_SIZE as tuple in form (SCREEN_WIDTH, SCREEN_HEIGHT)
#Return: a worldView object which:
#-world view has a shape(cube) 
#-has its own pygame surface object
#-has a render method to draw on its surface
#-activates needed chunks from the world given
#-Stores a list of hit boxes for objects rendered in list with elements in
# form: [pygame.Rect, Object]
class WorldView:
    def __init__(self, world, shape, SCREEN_SIZE):
        self.world       = world 
        self.shape       = shape 
        self.areaKeyList = self.shape.areaKeyList
        self.nD          = self.shape.nDimensionalArray
        self.prepareChunks() #Determine chunks needed and have world load them
        self.preloadCoordinates() #Overwrite self.nD with coordinates objects
        self.SCREEN_SIZE = SCREEN_SIZE
        self.surface     = pygame.Surface(SCREEN_SIZE) #Surface((width, height))
        self.hitBoxList  = []
    def prepareChunks(self):
        #Generate a list of chunks to activate
        chunks = []
        #For each coordinate key in self.area
        for coordKey in self.areaKeyList:
            #determine coordinates parent chunk
            parentChunk = findParent(coordKey)
            #check if chunk key is in the list...
            if parentChunk not in chunks: #If not...
                chunks.append(parentChunk)  #Add it...
        self.world.activateChunk(*chunks)
    def preloadCoordinates(self):
        for x in range(len(self.nD)):
            for y in range(len(self.nD[x])) :
                for z in range(len(self.nD[x][y])):
                    cKey = self.nD[x][y][z]
                    c = self.world.active[findParent(cKey)].coordinates[cKey]
                    self.nD[x][y][z] = c
    def render(self):
        self.surface.fill((0,0,0)) #Fill surface to avoid map edge slug trails 
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
                    if not c.empty: #Is this necessary if shape.z <= 0 only?
                        basepx = (x - y) * halfTileWide + PXOFFSET
                        basepy = (x + y) * halfTileHigh + PYOFFSET
                        for t in c.tiles:
                            px, py = basepx, (basepy)
                            img = TILE_MANIFEST[t.imageKey]
                            self.surface.blit(img, (px, py))
                            rect = Rect( (px,py), (img.get_width(),img.get_height() ) )
                            self.hitBoxList.append([rect, t])
        #Render everything else
        for y in yRange:
            for x in xRange:
                for z in range(len(self.nD[x][y])):
                        c = self.nD[x][y][z]
                        if not c.empty:#Is this necessary if shape.z <= 0 only?
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