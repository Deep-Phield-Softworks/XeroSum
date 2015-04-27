#!/usr/bin/env python
import random


from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping as pdict
from persistent.list import PersistentList as plist
import transaction


from unboundmethods import find_parent,  key_to_XYZ,  make_key
from chunk import Chunk
from subclassLoader import * #Temp commented out during rewrite
from aoe import Square 

#World objects have the following traits:
#-World object is not persistent. It is meant to be intitialized each session.
#-World object is a controller for persistent Chunk objects. Active Chunks are stored in self.active.
#-World receives the clock TICK, updates the game turn and sends the TICK to active Chunks.
#-World object opens the ZODB filestorage database and accesses its root. In the root, it looks for a key
# equal to its self.name.
class World:
    #Given: String name, and (optional) bool debug for verbose debug info, (optional) CHUNK_SIZE int list 
    #           defining XYZ dimensions of Chunk objects, and (optional) TILE_SIZE int list equal to 
    #           Tile [width, height] in pixels, db_file as optional string file name of DB
    #Return: World object
    def __init__(self, name, debug = False,  CHUNK_SIZE = [16,16,1], TILE_SIZE = [64, 32],  db_file = 'XSDB.fs'):
        self.name = name
        self.db_file = 'XSDB.fs'
        self.db = self.open(name,  db_file)
        self.init_args = {'CHUNK_SIZE': CHUNK_SIZE,
                                   'TILE_SIZE' : TILE_SIZE, 
                                   'active_chunks' :  pdict(),
                                   'chunks' :  pdict(),
                                   'game_turn' : 0, 
                                   'tick_accumulator' : 0 
                                 } 
        self.init(**self.init_args)

    #Given: key as string key to open in DB, db_file as string file name of DB to open 
    #Return: The given key to an OOBTree in given DB, making one if one doesn't already exist
    def open(self, key, db_file):
        db = DB(FileStorage.FileStorage(db_file))
        cnx = db.open()
        root = cnx.root()
        if not root.has_key(key):
            root[key] = OOBTree()
            transaction.commit()
        return root[key]

    #Given: **kwargs as a dictionary of string keys and any typed values. These entries will be
    #           stored in the top level of the World.db
    def init(self,  **kwargs):
        for key,  val in kwargs.iteritems():
            if not self.db.has_key(key):
                self.db[key] = val
        transaction.commit()
        
    #Given: No args
    #Close the chunks and save the DB    
    def close(self):
        self.deactivate_chunk(*self.db['active_chunks'].keys())
        transaction.commit()

    #Given: *keys as a list of Chunk object key strings for use in self.db['active_chunks']
    #Activates the given Chunk objects(loading their images ie) and creating new Chunks if needed.
    def activate_chunk(self, *keys):
        for key in keys:
            if not self.db['active_chunks'].has_key(key): #IF Chunk isn't active...
                if not self.db['chunks'].has_key(key): #If Chunk does NOT exists..
                    self.db['chunks'][key] = Chunk(key, self.gameTurn, self.CHUNK_SIZE) #Make it
                self.db['active_chunks'][key] = self.db['chunks'][key] #Add it to active Chunks    
                self.db['active_chunks'][key].load() #Have Chunk load itself
        transaction.commit()
    
    #Given: *keys as a list of Chunk object key strings for use in self.db['active_chunks']
    def deactivate_chunk(self, *keys):
        for key in keys:
            if self.db['active_chunks'].has_key(key): #IF Chunk is active...
                self.db['active_chunks'][key].unload()   #Unload Chunk
                self.db['chunks'][key] = self.db['active_chunks'][key] #Save Chunk back into DB (Necessary?)
                self.db['active_chunks'] = {keys:d[keys] for keys in d if keys != key} #Remove key from self.db['active_chunks']
        transaction.commit()

    #Given: int TICK as number of milliseconds that has passed since last time tick was called
    #Cascade the tick through all active Chunks
    ######NOTE#####
    #-Currently if TICK > 2000, only one turn will be taken and the TICK will become < 1000. Not sure this is the correct failure mode.
    #-TICK is being stored in ZODB. Not sure of performace ramifications here.
    def tick(self, TICK):
        self.db['tick_accumulator'] += TICK
        if self.db['tick_accumulator'] % 1000:
            self.db['game_turn'] += 1
            self.db['tick_accumulator'] = self.db['tick_accumulator'] % 1000
        for key in self.db['active_chunks'].keys():
            self.db['active_chunks'][key].tick(TICK, self.db['game_turn'])

    def addElement(self, coordinateKey, element):
        pchunk = find_parent(coordinateKey)
        self.activateChunk(pchunk)
        self.db['active_chunks'][pchunk].addElement(coordinateKey, element)

    def moveElement(self, element, aKey, bKey):
        #Make sure chunks are active
        aChunk = find_parent(aKey)
        bChunk = find_parent(bKey)
        self.activateChunk(aChunk)
        self.activateChunk(bChunk)
        self.db['active_chunks'][aChunk].removeElement(aKey, element)
        self.db['active_chunks'][bChunk].addElement(bKey, element)

    def getCoordinateObj(self, coordinateKey):
        parentChunk = find_parent(coordinateKey)
        self.activateChunk(parentChunk)
        return self.db['active_chunks'][parentChunk].coordinates[coordinateKey]

    def baseTerrainChunkFill(self, chunkKey, **kwargs):
        self.activateChunk(chunkKey)
        chunk = self.db['active_chunks'][chunkKey]
        origin = chunk.coordinatesList[0].key
        shapeargs = {'origin': origin, 'magnitude':self.CHUNK_SIZE}
        ground = Square(**shapeargs).areaKeyList
        for c in ground:
            chunk.coordinates[c].addElement(Tile(**kwargs))
    
    def randomFillChunkFeature(self, chunkKey, chance = 1, outOf = 10, **kwargs):
        self.activateChunk(chunkKey)
        for c in self.db['active_chunks'][chunkKey].coordinatesList:
            r = random.randint(0, outOf - 1)
            if r < chance:
                f = Feature(**kwargs)
                if not 'floatOffset' in kwargs: #If floatOffset not specified..
                    ranges = f.floatOffsetRanges #Get ranges..
                    f.floatOffset = [random.uniform(ranges[0][0],ranges[0][1]),
                                     random.uniform(ranges[1][0],ranges[1][1])]
                    #f.determinePixelOffset()
                f.determinePixelOffset()
                c.addElement(f)

if __name__ == "__main__":
    w = World('World1')
    print "\n"
    print "name: ",  w.name  
    print "db_file",  w.db_file
    for key,  val in w.db.iteritems():
        print key,  val
