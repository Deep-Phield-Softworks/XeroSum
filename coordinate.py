#!/usr/bin/env python
from persistent.list import PersistentList as plist


from unboundmethods import key_to_XYZ,  make_key
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
#-Coordinates can sort their contents by using floatOffsets (Deprecated, done in worldview.render())
#-Coordinates know whether their contents block Line of Sight

class Coordinate:
    def __init__(self, key):
        self.key = key
        self.XYZ = key_to_XYZ(key)
        self.x = self.XYZ[0]
        self.y = self.XYZ[1]
        self.z = self.XYZ[2]
        self.empty = True
        self.tiles  = plist([])
        self.features = plist([])
        self.items    = plist([])
        self.entities = plist([])
        self.fields   = plist([])
        self.parent_chunk  = make_key([self.x/16, self.y/16, self.z])
        self.blockLOS = False
    
    #Add an element to a list of corresponding types
    def add_element(self, element):
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
        element.coordinate_key = self.key
        self.updateLOS()

    #Remove an element
    def remove_element(self, element):
        if isinstance(element, Tile):
            if element in self.tiles:
                self.tiles.remove(element)
        if isinstance(element, Feature):
            if element in self.features:
                self.features.remove(element)
        if isinstance(element, Item):
            if element in self.items:
                self.items.remove(element)
        if isinstance(element, Entity):
            if element in self.entities:
                self.entities.remove(element)
        if isinstance(element, Field):
            if element in self.fields:
                self.fields.remove(element)
        element.parent_coordinate = None
        #Update self.empty boolean
        empty = True #Initialize to True
        for archetype in self.contains(): #For each list in self.contains()..
            if len(archetype) > 0:         #If len(list) > 0...
                empty = False              #Empty is false
                break                       #No need to continue... 
        self.empty = empty
        self.updateLOS()
    #Return a flat list of all contained elements
    def list_all(self):
        return self.tiles+self.features+self.items+self.entities+self.fields
        
    #Return ordered list of lists by object archetype.
    def contains(self):
        return [self.tiles, self.features, self.items, self.entities,  self.fields]
    
    def tick(self, TICK):
        #if not self.empty:
            for archetype in self.contains():
                for e in archetype:
                    e.tick(TICK)
    
    def updateLOS(self):
        blockLOS = False 
        elements = self.list_all()
        for e in elements:
            if hasattr(e, 'blocksLOS'):
                if e.blocksLOS:
                    blockLOS = True
                    break
        self.blockLOS = blockLOS
