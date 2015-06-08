#!/usr/bin/env python


from aoe import *
from unboundmethods import *


'''
Djikstra Map objects that can be combined together and can find paths
Given:
-shape, a shape template object from AoE.py
-selected_dict, a dictionary of coordinate Keys as dict keys and values that
 will be added to the DMAP
Return: a Djikstra Map object that:
-can be combined with other Djikstra Maps
-should be processed once all desired input DMAPs have been combined
-can return a list of nodes using find_path(start)
'''


class DijkstraMap:
    def __init__(self, shape, selected_dict, default_max=10000):
        self.shape = shape
        self.selected_dict = selected_dict
        # The coordinate keys are already in shape...
        # Use shape's nD Key list
        self.coordinates = self.shape.n_dimensional_array
        # Create a dictionary to store the values
        self.keys_flat_list = []
        self.map_vals = dict()
        # Populate the Map Values
        for x in xrange(0, len(self.coordinates)):
            for y in xrange(0, len(self.coordinates[x])):
                for z in xrange(0, len(self.coordinates[x][y])):
                        self.map_vals[self.coordinates[x][y][z]] = default_max
                        self.keys_flat_list.append(self.coordinates[x][y][z])
        for key in self.selected_dict.keys():
            if key in self.map_vals:
                self.map_vals[key] = self.selected_dict[key]
        # Using custom mods order to make diagonals "float to top" in paths
        self.mods = [(-1, -1, -1), (1, 1, -1), (-1, 1, -1), (1, -1, -1),
                     (0, -1, -1), (-1, 0, -1), (1, 0, -1), (0, 1, -1),
                     (-1, -1, 0), (1, 1, 0), (-1, 1, 0), (1, -1, 0),
                     (0, -1, 0), (-1, 0, 0), (1, 0, 0), (0, 1, 0),
                     (0, 0, 0), (-1, -1, 1), (1, 1, 1), (-1, 1, 1),
                     (1, -1, 1), (0, -1, 1), (-1, 0, 1), (1, 0, 1),
                     (0, 1, 1)]

    # You should call this ONLY once all desired inputs have been combined into
    # One DMAP. It must be called before using find_path().
    def process_map(self):
        again = True  # Control Boolean
        while(again):  # Run at least once
            again = False  # Set continue to false unless values change
            for key in self.keys_flat_list:
                if self.map_vals[key] != None:
                    low = self.lowest_neighbor_value(key)[0]
                    # PEP8 suggests 'if cond is not None'
                    if low:
                        if (self.map_vals[key] - low) >= 2:
                            self.map_vals[key] = low + 1
                            again = True

    # Returns the tuple of info on lowest neighbor it can find.
    def lowest_neighbor_value(self, key):
        low_key = None
        print "key", key
        XYZ = key_to_XYZ(key)
        for mod in self.mods:
            initial = [(XYZ[0] + mod[0]), (XYZ[1] + mod[1]), (XYZ[2] + mod[2])]
            trial_key = make_key(initial)
            # Use lazy and eval to avoid "no such key" exception here
            if trial_key in self.map_vals and self.map_vals[trial_key] != None:
                low = self.map_vals[trial_key]
                low_key = trial_key
                break
        for mod in self.mods:
            lookup = [None, None, None]
            lookup[0] = XYZ[0] + mod[0]
            lookup[1] = XYZ[1] + mod[1]
            lookup[2] = XYZ[2] + mod[2]
            modKey = make_key(lookup)
            if modKey in self.map_vals and self.map_vals[modKey] != None:
                if self.map_vals[modKey] <= low:
                    low = self.map_vals[modKey]
                    low_key = modKey
        return (low, low_key)

    def find_path(self, start_key):
        nodes = [start_key]
        next_node = self.lowest_neighbor_value(nodes[-1])[1]
        while(next_node is not None):
            next_node = self.lowest_neighbor_value(nodes[-1])[1]
            if next_node != nodes[-1]:
                nodes.append(next_node)
            else:
                break
        return nodes

    # Add together the values of two DMAPS. If a given coordinate is None in
    # either DMAP it becomes None. Otherwise the values of both are added.
    def combine(self, DMAP):
        for key in self.keys_flat_list:  # For key in self..
            if key in DMAP.map_vals:  # If key in DMAP...
                if DMAP.map_vals[key] == None or self.map_vals[key] == None:
                    self.map_vals[key] = None  # Set value
                else:
                    self.map_vals[key] += DMAP.map_vals[key]
        return self

    # Combine two DMAPs. Then expand the calling DMAP by the unique coordinates
    # in the argument DMAP.
    def expand(self, DMAP):
        # First combine the cells they have in common
        self = self.combine(DMAP)
        # Add new keys from DMAP
        for key in DMAP.keys_flat_list:  # F or key in DMAP
            if key not in self.map_vals:  # If key not in self
                # Add key & value to self
                self.map_vals[key] = DMAP.map_vals[key]
                # Add key to flat list
                self.keys_flat_list.append(key)
        # Lastly make a new expanded DMAP, populating the empty cells w/ None
        self_bounds = self.bounds()  # Find the bounds
        DMAP_bounds = DMAP.bounds()
        # Find the origin
        origin = make_key(self.lower(self_bounds, DMAP_bounds))
        magnitude = (abs(self_bounds[0] - DMAP_bounds[0]),
                     abs(self_bounds[1] - DMAP_bounds[1]),
                     abs(self_bounds[2] - DMAP_bounds[2]))
        new_shape = Cube(origin, magnitude, True)  # Create a new Shape
        expanded = DijkstraMap(new_shape, self.map_vals, None)
        return expanded

    # Define the bounaries as a pair of lowest (x,y,z) and greatest
    # (x,y,z) values as determiend by using the calling DMAP's self.coordinates
    def bounds(self):
        low = key_to_XYZ(self.coordinates[0][0][0])
        hi = key_to_XYZ(self.coordinates[-1][-1][-1])
        return (low, hi)

    # Given two points in form: (x,y,z)
    # Return: Lower of the two points
    def lower(self, a, b):
        low = a
        if a[0] > b[0]:
            low = b
        elif a[1] > b[1]:
            low = b
        elif a[2] > b[2]:
            low = b
        return low

if __name__ == '__main__':
    # Run a test
    # Make a key to use in shape object creation
    origin = [0, 0, 0]
    oKey = make_key(origin)
    # Make a Cube shape object
    # Shape will extend from (0,0,0) to (20,20,0) in cube shape
    shape = Cube(oKey, [21, 21, 1], True)
    # Dictionary of selected cells and their values.
    # Value of 0 is a goal, None is impassible
    selected_dict = dict()
    selected_dict['10_10_0'] = 0
    selected_dict['1_1_0'] = None
    # Create the Dijkstra Map
    d = DijkstraMap(shape, selected_dict)
    # Optionally Combine other DMAPs if desired
    # d.combine(otherDMAP)
    # After all DMAPs are combined, process once
    d.process_map()
    # Find a path given a start point
    print d.find_path('0_0_0')
    print "Bounds"
    print d.bounds()
