#!/usr/bin/env python
from operator import itemgetter


from pygame import Rect, Surface
from BTrees.OOBTree import OOBTree


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
    def __init__(self, screen, world, shape_args, px_offset,  py_offset,
                 TILE_WIDTH=64, TILE_HEIGHT=32):
        self.world = world
        self.screen = screen
        self.screen_size = screen.get_size()
        self.chunks = []
        self.shape = Cuboid(**shape_args)
        self.px_offset = px_offset
        self.py_offset = py_offset
        self.TILE_WIDTH = TILE_WIDTH
        self.TILE_HEIGHT = TILE_HEIGHT
        self.render_key_list = self.shape.render_key_list
        self.nD = self.shape.shaped_3d_array
        self.background = Surface(self.screen_size)
        self.text = Surface((120, 40))
        self.text_pxy = (0, (self.screen_size[1] - self.text.get_size()[1]))
        self.loaded = {}
        # Determine chunks needed and have world load them
        self.prepare_chunks()
        # Overwrite self.nD with coordinates objects
        self.preload()
        self.rects = []
        self.b = OOBTree()
        self.e = OOBTree()
        self.init_b()

    def prepare_chunks(self):
        '''Generate a list of chunks in view. Ensure they are created.'''
        for key in self.render_key_list:
            parent_chunk = find_parent(key)
            if parent_chunk not in self.chunks:
                self.chunks.append(parent_chunk)
                self.world.get_chunk(parent_chunk)

    def preload(self):
        '''Pre-calculate the on screen position and load each coordinate.
        Sort each element into background or foreground. Blit all the
        tiles onto the background surface.
        '''
        half_tile_wide = int(self.TILE_WIDTH / 2)
        half_tile_high = int(self.TILE_HEIGHT / 2)
        for x in xrange(len(self.nD)):
            for y in xrange(len(self.nD[x])):
                for z in xrange(len(self.nD[x][y])):
                    cKey = self.nD[x][y][z]
                    chunk = self.world.db['chunks'][find_parent(cKey)]
                    c = chunk.coordinates[cKey]
                    px = (x - y) * half_tile_wide + self.px_offset
                    py = (x + y) * half_tile_high + self.py_offset
                    self.loaded[cKey] = [c, px, py]
                    for t in c.tiles:
                        self.background.blit(t.to_blit(), (px, py))

    def init_b(self):
        self.screen.blit(self.background, (0, 0))
        for cKey in self.loaded:
                    c = self.loaded[cKey][0]
                    px = self.loaded[cKey][1]
                    py = self.loaded[cKey][2]
                    for e in c.list_all():
                        if e.layer > 0.1:
                            img = e.to_blit()
                            px = px + e.pixel_offsets[0]
                            py = py + e.pixel_offsets[1]
                            rect = Rect((px, py), (img.get_width(),
                                                   img.get_height()))
                            k = (e.layer, py, px, e)
                            self.b[k] = e
                            self.e[e] = k

    def render(self):
        self.screen.blit(self.text, self.text_pxy)
        self.e_on_screen = 0
        self.rects = []
        remove = []
        for cKey in self.loaded:
            c = self.loaded[cKey][0]
            px = self.loaded[cKey][1]
            py = self.loaded[cKey][2]
            for e in c.list_all():
                self.e_on_screen += 1
                if e.layer > 0.1:
                    img = e.to_blit()
                    px = px + e.pixel_offsets[0]
                    py = py + e.pixel_offsets[1]
                    rect = Rect((px, py), (img.get_width(),
                                           img.get_height()))
                    k = (e.layer, py, px, e)
                    if k not in self.b:
                        self.b[k] = e
                        if e in self.e:
                            remove.append(self.e[k])
                        self.b[e] = k
        for r in remove:
            self.b.remove(r)
        for k in self.b:
            e = self.b[k]
            self.screen.blit(e.to_blit(), (k[2], k[1]))

    def render_old(self):
        # Fill surface to avoid map edge slug trails
        self.screen.fill((0, 0, 0))
        # Empty hit_box_list
        self.hit_box_list = []
        unsorted = []
        x_range = xrange(len(self.nD))
        y_range = xrange(len(self.nD[0]))
        # Render Tiles
        self.e_on_screen = 0
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
            self.e_on_screen += 1
            self.screen.blit(e[0], (e[3], e[2]))
