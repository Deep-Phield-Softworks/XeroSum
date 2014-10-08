#!/usr/bin/env python
import shelve, random
from unboundMethods import *
from Chunk import Chunk
from subclassLoader import *
from AoE import *
#World object is a controller for Chunk objects. 
#Active Chunks are stored in self.active. Inactive Chunks are saved in the db.
#World receives the clock TICK, updates the game turn and sends the TICK to
#active Chunks.
#World creating Chunks according to an minimap terrain type template.
class World:
    def __init__(self, name, chunkSize = [16,16,1]):
        self.name = name
        self.chunkSize = chunkSize
        self.db = str(name) + "Shelf"
        self.active = dict()
        self.gameTurn = 0
        self.tickAccumulator = 0
    def baseTerrainChunkFill(self, chunkKey, baseArgs):
        self.activateChunk(chunkKey)
        chunk = self.active[chunkKey]
        origin = chunk.coordinatesList[0].key
        ground = Square(origin, self.chunkSize, True).areaKeyList
        for c in ground:
            chunk.coordinates[c].addElement(Tile(*baseArgs))
    def randomFillChunkFeature(self, chunkKey, objArgs, chance = 1, outOf = 10):
        self.activateChunk(chunkKey)
        for c in self.active[chunkKey].coordinatesList:
            r = random.randint(0,outOf - 1)
            if r < chance:
                f = Feature(*objArgs)
                f.floatOffset = [random.random(),random.random()]
                f.determinePixelOffset()
                c.addElement(f)
    def activateChunk(self, *keys):
        for key in keys:
            if not self.active.has_key(key):
                db = shelve.open(self.db)
                if db.has_key(key): #If Chunk exists..
                    self.active[key] = db[key] #Load it into active Chunks
                else:               #Else if Chunk doesn't exist
                    self.active[key] = Chunk(key, self.gameTurn, self.chunkSize) #Make it and load it
                    db[key] = self.active[key] #Save chunk in db
                db.close()
                self.active[key].load()
    def deactivateChunk(self, *keys):
        for key in keys:
            self.active[key].unload()
            db = shelve.open(self.db)
            db[key] = self.active[key]
            db.close()
    def TICK(self, TICK):
        self.tickAccumulator += TICK
        if self.tickAccumulator % 1000:
            self.gameTurn += 1
            self.tickAccumulator = self.tickAccumulator % 1000
        for chunkKey in self.active.keys():
            self.active[chunkKey].TICK(TICK, self.gameTurn)
    def addElement(self, coordinateKey, element):
        pchunk = findParent(coordinateKey)
        self.activateChunk(pchunk)
        self.active[pchunk].addElement(coordinateKey, element)
    def addEntity(self, *entityConstructorArgs):
        e = Entity(*entityConstructorArgs)
        pchunk = findParent(e.coordinateKey)
        self.activateChunk(pchunk)
        self.active[pchunk].addElement(e.coordinateKey, e)
    def moveElement(self, element, aKey, bKey):
        #Make sure chunks are active
        aChunk = findParent(aKey)
        bChunk = findParent(bKey)
        self.activateChunk(aChunk)
        self.activateChunk(bChunk)
        self.active[aChunk].removeElement(aKey, element)
        self.active[bChunk].addElement(bKey, element)
    def getCoordinateObj(self, coordinateKey):
        parentChunk = findParent(coordinateKey)
        self.activateChunk(parentChunk)
        return self.active[parentChunk].coordinates[coordinateKey]