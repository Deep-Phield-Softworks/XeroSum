#!/usr/bin/env python

from random import uniform, randint


from ZODB import FileStorage, DB
from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping as pdict
from persistent.list import PersistentList as plist
import transaction


from unboundmethods import find_parent,  key_to_XYZ,  make_key
from chunk import Chunk
from tile import Tile
from feature import Feature
from aoe import Cuboid


class World:
    def __init__(self, name, debug=False,  CHUNK_SIZE=[16, 16, 1],
                 TILE_SIZE=[64, 32],  db_file='XSDB.fs'):
        self.name = name
        self.db_file = 'XSDB.fs'
        self.db = self.open(name,  db_file)
        self.init_args = {'CHUNK_SIZE': CHUNK_SIZE,
                          'TILE_SIZE': TILE_SIZE,
                          'tick_roster': OOBTree(),
                          'effect_queue': plist(),
                          'chunks': OOBTree(),
                          'game_turn': 0,
                          'play_music': False,
                          'turn_accumulator': 0,
                          'new_game': True,
                          'player': None}
        self.db_init(**self.init_args)

    def open(self, key, db_file):
        '''Open the ZODB FileStorage and return the World's root.'''
        db = DB(FileStorage.FileStorage(db_file))
        cnx = db.open()
        root = cnx.root()
        # PEP8 has_key is deprecated, use 'in'
        if key not in root:
            root[key] = OOBTree()
            transaction.commit()
        return root[key]

    def db_init(self,  **kwargs):
        '''Initalize db and create entries as needed.'''
        for key,  val in kwargs.iteritems():
            if key not in self.db:
                self.db[key] = val
        transaction.commit()

    def close(self):
        transaction.commit()

    '''
    Given: int TICK as number of milliseconds that has passed since last time
    tick was called. Cascade the tick through all active Chunks
    ######NOTE#####
    -Currently if TICK > 2000, only one turn will be taken and the TICK will
    become < 1000. Not sure this is the correct failure mode.
    -TICK is being stored in ZODB. Not sure of performace ramifications here.
    '''
    def tick(self, TICK):
        self.db['turn_accumulator'] += TICK  # Increment tick accumulator
        if self.db['turn_accumulator'] % 1000:  # If % 1000 leaves a remainder
            self.db['game_turn'] += 1  # Increment game turn
            # Get tick accumulator remainder
            self.db['turn_accumulator'] = self.db['turn_accumulator'] % 1000
        '''for key in self.db['chunks'].keys():
            self.db['chunks'][key].tick(TICK, self.db['game_turn'])'''

    '''
    Given: coordinate_key as string and an object reference as element
    Add (probably new) element to a Coordinate object's contents
    '''
    def add_element(self, coordinate_key, element):
        pchunk = find_parent(coordinate_key)
        self.db['chunks'][pchunk].add_element(coordinate_key, element)
        transaction.commit()

    """
    Add effects to a persistent list. Requires effects to be in
    form [effect, target] for use with World.add_effect().
    """
    def queue_effects(self, *effects):
        for e in effects:
            self.db['effect_queue'].append(e)

    """
    Process all queued effects. Effects are processed FILO as lists
    aren't efficient to pop() from front.
    """
    def process_effects(self):
        while self.db['effect_queue']:
            self.add_effect(*self.db['effect_queue'].pop())

    """
    Add an effect to target and add target to the tick roster.
    """
    def add_effect(self, effect, target):
        if hasattr(target, 'effects'):
            target.effects.append(effect)
            if target not in self.db['tick_roster']:
                self.db['tick_roster'][target] = target

    '''
    Given: element as an object reference, and aKey and bKey as Coordinate
    object key strings. Move element from Coordinate aKey to Coordinate bKey
    '''
    def move_element(self, element, aKey, bKey):
        # Find Chunks involved
        aChunk = find_parent(aKey)
        bChunk = find_parent(bKey)
        # Remove from aKey
        self.db['chunks'][aChunk].remove_element(aKey, element)
        # Move to bKey
        self.db['chunks'][bChunk].add_element(bKey, element)
        transaction.commit()

    def activate_elements(self, *elements):
        for e in elements:
            if e not in self.db['tick_roster']:
                self.db['tick_roster'][e] = e

    def get_coordinate_obj(self, key):
        '''Return Coordinate object.'''
        return self.db['chunks'][find_parent(key)].coordinates[key]

    def get_chunk(self, key):
        if key not in self.db['chunks']:
            self.db['chunks'][key] = Chunk(
                            key,
                            self.db['game_turn'],
                            self.db['CHUNK_SIZE']
                                          )
        return self.db['chunks'][key]

    '''
    Given: chunk_key as Chunk object key string, **tile_args as
    a **kwarg dict of Tile object creation arguements
    Make a terrain layer of Tile objects for the given Chunk
    '''
    def chunk_terrain_base_fill(self, chunk_key, **tile_args):
        chunk = self.db['chunks'][chunk_key]
        # Get chunk Coordinate object origin
        origin_key = chunk.coordinates_list[0].key
        o = key_to_XYZ(origin_key)
        size = self.db['CHUNK_SIZE']
        magnitude = [(o[i] + size[i]) for i in xrange(len(o))]
        # Make a dict of shape args
        shape_args = {'origin': o, 'magnitude':  magnitude}
        # Make a shape that includes all the Chunk's Coordinates
        ground = Cuboid(**shape_args).render_key_list
        for c in ground:  # For each Coordinate
            # Add a Tile object made with **tile_args as the arguements
            chunk.coordinates[c].add_element(Tile(**tile_args))

    '''
    Given: chunk_key as Chunk object key string, chance  and out_of as ints
    to control probability per Coordinate of placing feature,
    and **feature_args as a **kwarg dict of Feature object creation
    arguements
    Create and place randomly Feature objects in the given Chunk
    '''
    def chunk_random_feature_fill(self, chunk_key, chance=1,
                                  out_of=10, **feature_args):
        for c in self.db['chunks'][chunk_key].coordinates_list:
            r = randint(0, out_of - 1)
            if r < chance:
                f = Feature(**feature_args)
                # If floatOffset not specified
                if 'float_offset' not in feature_args:
                    ranges = f.float_offset_ranges  # Get ranges..
                    f.float_offset = [uniform(ranges[0][0],
                                              ranges[0][1]),
                                      uniform(ranges[1][0],
                                              ranges[1][1])]
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
