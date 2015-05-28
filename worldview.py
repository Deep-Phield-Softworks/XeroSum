#!/usr/bin/env python
from operator import *


from pygame import Rect, Surface


from aoe import Cuboid
from unboundmethods import find_parent

'''
worldView is an object made to render a portion of the world.
Given:
-world object
-shape object
-screen_size as tuple in form (SCREEN_WIDTH, SCREEN_HEIGHT)
Return: a worldView object which:
-world view has a shape(cube)
-has its own pygame surface object
-has a render method to draw on its surface
-activates needed chunks from the world given
-stores a list of hit boxes for objects rendered in list with elements in
 form: [pygame.Rect, Object]
'''


class WorldView:
    def __init__(self, world, shape_args, screen_size, px_offset,  py_offset,
                 TILE_WIDTH=64, TILE_HEIGHT=32):
        self.world = world
        self.shape = Cuboid(**shape_args)
        self.px_offset = px_offset
        self.py_offset = py_offset
        self.TILE_WIDTH = TILE_WIDTH
        self.TILE_HEIGHT = TILE_HEIGHT
        self.render_key_list = self.shape.render_key_list
        self.nD = self.shape.shaped_3d_array
        # Determine chunks needed and have world load them
        self.prepare_chunks()
        # Overwrite self.nD with coordinates objects
        self.preload_coordinates()
        self.screen_size = screen_size
        # Surface((width, height))
        self.surface = Surface(screen_size)
        self.hit_box_list = []

    def prepare_chunks(self):
        # Generate a list of chunks to activate
        chunks = []
        # For each coordinate key in self.area
        for coord_key in self.render_key_list:
            # determine coordinates parent chunk
            parent_chunk = find_parent(coord_key)
            # check if chunk key is in the list...
            if parent_chunk not in chunks:  # If not...
                chunks.append(parent_chunk)  # Add it...
        self.world.activate_chunk(*chunks)

    def preload_coordinates(self):
        half_tile_wide = int(self.TILE_WIDTH / 2)
        half_tile_high = int(self.TILE_HEIGHT / 2)
        for x in range(len(self.nD)):
            for y in range(len(self.nD[x])):
                for z in range(len(self.nD[x][y])):
                    cKey = self.nD[x][y][z]
                    chunk = self.world.db['active_chunks'][find_parent(cKey)]
                    c = chunk.coordinates[cKey]
                    basepx = (x - y) * half_tile_wide + self.px_offset
                    basepy = (x + y) * half_tile_high + self.py_offset
                    self.nD[x][y][z] = c, (basepx, basepy)

    def render(self):
        # Fill surface to avoid map edge slug trails
        self.surface.fill((0, 0, 0))
        # Empty hit_box_list
        self.hit_box_list = []
        unsorted = []
        x_range = range(len(self.nD))
        y_range = range(len(self.nD[0]))
        # Render Tiles
        for y in y_range:
            for x in x_range:
                for z in range(len(self.nD[x][y])):
                    c = self.nD[x][y][z][0]  # c is now the Coordinate object
                    px = self.nD[x][y][z][1][0]
                    py = self.nD[x][y][z][1][1]
                    contents = c.list_all()  # get all contents
                    for e in contents:
                        # Determine proper image
                        img = e.to_blit()
                        # Adjust px,py based upon e's attributes
                        px = px + e.pixel_offsets[0]
                        py = py + e.pixel_offsets[1]
                        # Create hit box rect and add to hit_box_list
                        rect = Rect((px, py), (img.get_width(),
                                               img.get_height()))
                        self.hit_box_list.append([rect, e])
                        unsorted.append([img, e.layer, py, px, e])
        # Sort render elements by layer, py, px
        render_list = sorted(unsorted, key=itemgetter(1, 2, 3))
        for e in render_list:
            self.surface.blit(e[0], (e[3], e[2]))
