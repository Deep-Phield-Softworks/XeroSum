#!/usr/bin/env python
from unboundmethods import *
from tile import Tile
from feature import Feature
from item import Item
from entity import Entity
from field import Field


#Coordinates objects represent a location in a x,y,z coordinate plane.
#Coordinates have the properties:
#-Low level container of the other data object types
#-The chunk that contains a given coordinate can be determined mathematically
# by using integer division of the coordinate's (x,y,z) by the chunkSize
#-Coordinates know whether they are empty or not
#-Coordinates have a list for each base type they can contain
#-Coordinates can be told to add elements of the base types and will add them
# to the respective list
#-Coordinates can return their contents by using the contains() method
#-Coordinates can tick their contents
#-Coordinates can sort their contents by using floatOffsets
#-Coordinates know whether their contents block Line of Sight
class Coordinate:
    def __init__(self, key):
        self.key = key
        self.XYZ = keyToXYZ(key)
        self.x = self.XYZ[0]
        self.y = self.XYZ[1]
        self.z = self.XYZ[2]
        self.empty = True
        self.tiles  = []
        self.features = []
        self.items    = []
        self.entities = []
        self.fields   = []
        self.parentChunk  = makeKey([self.x/16, self.y/16, self.z])
        self.blockLOS = False
    #Add an element to a list of corresponding types
    def addElement(self, element):
        self.empty = False
        if isinstance(element, Tile):
            self.tiles.append(element)
        if isinstance(element, Feature):
            self.features.append(element)
        if isinstance(element, Item):
            self.items.append(element)
        if isinstance(element, Entity):
            self.entities.append(element)
        if isinstance(element, Field):
            self.fields.append(element)
        element.parentCoordinate = self.key
        self.updateLOS()
        #self.orderContents()
    #Remove an element
    def removeElement(self, element):
        if isinstance(element, Tile):
            #if element in self.tiles:
                self.tiles.remove(element)
        if isinstance(element, Feature):
            #if element in self.features:
                self.features.remove(element)
        if isinstance(element, Item):
            #if element in self.items:
                self.items.remove(element)
        if isinstance(element, Entity):
            #if element in self.entities:
                self.entities.remove(element)
        if isinstance(element, Field):
            #if element in self.fields:
                self.fields.remove(element)
        element.parentCoordinate = None
        #Update self.empty boolean
        empty = True #Initializze to True
        for archtype in self.contains(): #For each list in self.contains()..
            if len(archtype) > 0:         #If len(list) > 0...
                empty = False              #Empty is false
                break                       #No need to continue... 
        self.empty = empty
        self.updateLOS()
    #Return a flat list of all contained elements
    def listAll(self):
        elements = self.tiles+self.features+self.items+self.entities+self.fields
        return elements
    #Return ordered list of lists by object archetype.
    def contains(self):
        contents = []
        contents.append(self.tiles)
        contents.append(self.features)
        contents.append(self.items)
        contents.append(self.entities)
        contents.append(self.fields)
        return contents
    def TICK(self, TICK):
        if not self.empty:
            for archtype in self.contains():
                for e in archtype:
                    e.TICK(TICK)
    def load(self):
        #if not self.empty:
        for e in self.entities:
            e.load()
    def unload(self):
        #if not self.empty:
        for e in self.entities:
            e.unload()
    def updateLOS(self):
        blockLOS = False 
        elements = self.listAll()
        for e in elements:
            if hasattr(e, 'blocksLOS'):
                if e.blocksLOS:
                    blockLOS = True
                    break
        self.blockLOS = blockLOS
        pass
