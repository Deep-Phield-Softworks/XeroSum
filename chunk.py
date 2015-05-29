#!/usr/bin/env python
from persistent.mapping import PersistentMapping as pdict
from persistent.list import PersistentList as plist
from unboundmethods import key_to_XYZ, make_key
from coordinate import Coordinate


'''
Chunk objects are containers for organizing coordinates into sets that are
either active or inactive. Chunks have the following properties:
    -They are bounded planes composed of ordered sets of coordinates
    -Each chunk is of uniform dimensions in x, y and z axis
    -No two chunks can contain the same coordinate object
    -Active chunks receive ticks
    -Inactive chunks store the last game turn they were active
    -The chunk that contains a given coordinate can be determined
    mathematically by using integer division of the coordinate's
    (x,y,z) by the chunkSize
'''


class Chunk:

    def __init__(self, key, game_turn, chunk_size=[16, 16, 1]):
        self.key = key
        self.XYZ = key_to_XYZ(key)
        self.chunk_size = chunk_size
        self.game_turn_created = game_turn
        self.coordinates = pdict()
        self.coordinates_list = plist()
        self.chunk_range = self.define_chunk_range()
        self.make_coordinates(self.chunk_range)
        self.last_active_game_turn = self.game_turn_created

    def define_chunk_range(self):
        x = self.XYZ[0] * 16
        y = self.XYZ[1] * 16
        z = self.XYZ[2]  # * 16
        xRange = [x, x + (self.chunk_size[0])]
        yRange = [y, y + (self.chunk_size[1])]
        zRange = [z, z + (self.chunk_size[2])]
        return [xRange, yRange, zRange]

    def make_coordinates(self, ranges):
        for x in range(*ranges[0]):
            for y in range(*ranges[1]):
                for z in range(*ranges[2]):
                    key = make_key([x, y, z])  # Make a key string
                    # Make coordinate object and store it
                    c = Coordinate(key)
                    self.coordinates[key] = c
                    self.coordinates_list.append(c)

    def tick(self, TICK, game_turn):
        self.last_active_game_turn = game_turn
        for c in self.coordinates_list:
            c.tick(TICK)

    def add_element(self, coordinate_key, element):
        self.coordinates[coordinate_key].add_element(element)

    def remove_element(self, coordinate_key, element):
        self.coordinates[coordinate_key].remove_element(element)
