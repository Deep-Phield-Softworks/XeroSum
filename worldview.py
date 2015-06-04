#!/usr/bin/env python
from operator import itemgetter


from pygame import Rect, Surface, display
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
    def __init__(self, world, shape_args, px_offset,  py_offset,
                 font, clock, TILE_WIDTH=64, TILE_HEIGHT=32):
        self.world = world
        self.screen = display.get_surface()
        self.screen_size = self.screen.get_size()
        self.font = font
        self.font_height = self.font.get_linesize()
        self.text = Surface((120, 40))
        self.clock = clock
        self.text_pxy = (0, (self.screen_size[1] - self.text.get_size()[1]))
        self.text_rect = Rect((self.text_pxy), (120, 40))
        self.px_offset = px_offset
        self.py_offset = py_offset
        self.TILE_WIDTH = TILE_WIDTH
        self.TILE_HEIGHT = TILE_HEIGHT
        self.chunks = []
        self.shape = Cuboid(**shape_args)
        self.render_key_list = self.shape.render_key_list
        self.nD = self.shape.shaped_3d_array
        self.background = Surface(self.screen_size)
        self.loaded = {}
        self.prepare_chunks()
        self.preload()
        self.rects = []
        self.dirty = []
        self.iso = OOBTree()
        self.elements = OOBTree()
        self.e_on_screen = 0
        self.screen_text = []

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
        self.screen.blit(self.background, (0, 0))

    def draw_screen_text(self):
        self.screen_text = []
        elements = "Elements = " + str(self.e_on_screen)
        self.screen_text.append(elements)
        fps = "FPS = " + str(self.clock.get_fps())
        self.screen_text.append(fps)
        y = self.screen_size[1] - self.font_height
        for text in reversed(self.screen_text):
            self.screen.blit(self.font.render(text, True, (255, 0, 0)), (0, y))
            y -= self.font_height

    def render(self):
        self.screen.blit(self.text, self.text_pxy)
        self.e_on_screen = 0
        self.rects = []
        self.dirty = []
        self.redraw = OOBTree()
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
                    self.rects.append(rect)
                    k = (e.layer, py, px, e)
                    if k not in self.iso:
                        self.iso[k] = e
                        self.redraw[k] = e
                        self.dirty.append(rect)
                        if e in self.elements:
                            self.dirty.append(e[-1])
                            remove.append(self.elements[e])
                        self.elements[e] = (k, rect)
        for r in remove:
            self.iso.remove(r)
        for k in self.redraw:
            e = self.iso[k]
            self.screen.blit(e.to_blit(), (k[2], k[1]))
        if bool(len(self.dirty)) or bool(len(self.screen_text)):
            display.update(self.dirty)
            display.flip()
