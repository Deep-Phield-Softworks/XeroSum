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
        self.coordinates = {}
        self.coordinates_list = []
        self.chunk_range = self.define_chunk_range()
        self.make_coordinates(self.chunk_range)
        self.last_active_game_turn = self.game_turn_created
        self.active_elements = plist([])

    def define_chunk_range(self):
        x = self.XYZ[0] * 16
        y = self.XYZ[1] * 16
        z = self.XYZ[2]  # * 16
        x_range = [x, x + (self.chunk_size[0])]
        y_range = [y, y + (self.chunk_size[1])]
        z_range = [z, z + (self.chunk_size[2])]
        return [x_range, y_range, z_range]

    def make_coordinates(self, ranges):
        for x in xrange(*ranges[0]):
            for y in xrange(*ranges[1]):
                for z in xrange(*ranges[2]):
                    key = make_key([x, y, z])  # Make a key string
                    # Make coordinate object and store it
                    c = Coordinate(key)
                    self.coordinates[key] = c
                    self.coordinates_list.append(c)

    def add_element(self, coordinate_key, element):
        if not element.passive:
            self.active_elements[element] = element
        self.coordinates[coordinate_key].add_element(element)

    def remove_element(self, coordinate_key, element):
        if not element.passive:
            if element in self.active_elements:
                del self.active_elements[element]
        self.coordinates[coordinate_key].remove_element(element)
