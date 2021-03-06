#!/usr/bin/env python
import random


from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping as pdict
from persistent.list import PersistentList as plist
import transaction


from unboundmethods import find_parent,  key_to_XYZ,  make_key
from chunk import Chunk
from subclassloader import * #Temp commented out during rewrite
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
                                   'play_music': True,  
                                   'tick_accumulator' : 0, 
                                   'new_game': True, 
                                   'player': None
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
                    self.db['chunks'][key] = Chunk(key, self.db['game_turn'], self.db['CHUNK_SIZE']) #Make it
                self.db['active_chunks'][key] = self.db['chunks'][key] #Add it to active Chunks    
        transaction.commit()
    
    #Given: *keys as a list of Chunk object key strings for use in self.db['active_chunks']
    def deactivate_chunk(self, *keys):
        for key in keys:
            if self.db['active_chunks'].has_key(key): #IF Chunk is active...
                #self.db['active_chunks'][key].unload()   #Unload Chunk
                self.db['chunks'][key] = self.db['active_chunks'][key] #Save Chunk back into DB (Necessary?)
                self.db['active_chunks'] = {keys:self.db['active_chunks'][keys] for keys in self.db['active_chunks'] if keys != key} #Remove key from self.db['active_chunks']
        transaction.commit()

    #Given: int TICK as number of milliseconds that has passed since last time tick was called
    #Cascade the tick through all active Chunks
    ######NOTE#####
    #-Currently if TICK > 2000, only one turn will be taken and the TICK will become < 1000. Not sure this is the correct failure mode.
    #-TICK is being stored in ZODB. Not sure of performace ramifications here.
    ######NOTE#####
    def tick(self, TICK):
        self.db['tick_accumulator'] += TICK #Increment tick accumulator
        if self.db['tick_accumulator'] % 1000: #If % 1000 leaves a remainder...
            self.db['game_turn'] += 1                        #Increment game turn 
            self.db['tick_accumulator'] = self.db['tick_accumulator'] % 1000 #Get tick accumulator remainder
        for key in self.db['active_chunks'].keys(): #For each active chunk
            self.db['active_chunks'][key].tick(TICK, self.db['game_turn'])  #Cascade the game turn

    #Given: coordinate_key as string and an object reference as element
    #Add (probably new) element to a Coordinate object's contents
    def add_element(self, coordinate_key, element):
        pchunk = find_parent(coordinate_key)
        self.activate_chunk(pchunk)
        self.db['active_chunks'][pchunk].add_element(coordinate_key, element)
        transaction.commit()

    #Given: element as an object reference, and aKey and bKey as Coordinate object key strings
    #Move element from Coordinate aKey to Coordinate bKey
    def move_element(self, element, aKey, bKey):
        #Find Chunks involved
        aChunk = find_parent(aKey)
        bChunk = find_parent(bKey)
        self.activate_chunk(aChunk,  bChunk) #Make sure they are active
        self.db['active_chunks'][aChunk].remove_element(aKey, element) #Remove from aKey
        self.db['active_chunks'][bChunk].add_element(bKey, element)       #Move to bKey
        transaction.commit()

    #Given: coordinate_key as Coordinate object key string
    #Return: Coordinate object's reference
    def get_coordinate_obj(self, coordinate_key):
        return self.db['chunks'][find_parent(coordinate_key)].coordinates[coordinate_key]

    #Given: chunk_key as Chunk object key string, **tile_args as a **kwarg dict of Tile object creation arguements
    #Make a terrain layer of Tile objects for the given Chunk
    def chunk_terrain_base_fill(self, chunk_key, **tile_args):
        self.activate_chunk(chunk_key) #Activate the Chunk
        chunk = self.db['active_chunks'][chunk_key]  #Assign to variable chunk for clarity
        origin = chunk.coordinates_list[0].key                  #Get chunk Coordinate object origin
        shape_args = {'origin': origin, 'magnitude':self.db['CHUNK_SIZE']} #Make a dict of shape args
        ground = Square(**shape_args).area_key_list #Make a shape that includes all the Chunk's Coordinates
        for c in ground: #For each Coordinate
            chunk.coordinates[c].add_element(Tile(**tile_args)) #Add a Tile object made with **tile_args as the arguements
    
    #Given: chunk_key as Chunk object key string, chance  and out_of as ints to control probability per Coordinate of 
    #           placing feature, and **feature_args as a **kwarg dict of Feature object creation arguements
    #Create and place randomly Feature objects in the given Chunk
    def chunk_random_feature_fill(self, chunk_key, chance = 1, out_of = 10, **feature_args):
        self.activate_chunk(chunk_key)
        for c in self.db['active_chunks'][chunk_key].coordinates_list:
            r = random.randint(0, out_of - 1)
            if r < chance:
                f = Feature(**feature_args)
                if not 'float_offset' in feature_args: #If floatOffset not specified..
                    ranges = f.float_offset_ranges #Get ranges..
                    f.float_offset = [random.uniform(ranges[0][0],ranges[0][1]),
                                              random.uniform(ranges[1][0],ranges[1][1])]
                f.determine_pixel_offset()
                c.add_element(f)
    
    def close(self):
        transaction.commit()

if __name__ == "__main__":
    w = World('World1')
    print "\n"
    print "name: ",  w.name  
    print "db_file",  w.db_file
    for key,  val in w.db.iteritems():
        print key,  val
