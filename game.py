#!/usr/bin/env python
import sys
import os
import random


import pygame
import transaction


from controller import Controller
from manifests import screen, screen_size, tracks, COLORKEY, ui_manifest
from world import World
from player import Player
from aoe import *
from worldview import WorldView
from path import Path
from entity import Entity
from unboundmethods import key_to_XYZ, find_parent
from unboundmethods import adjacent, find_adjacents
from unboundmethods import TILE_WIDTH, TILE_HEIGHT

"""
Game Class for Xero Sum
Game is a high level wrapper that has the following attributes:
-Initializes pygame and pygame sound mixer
-Has convenience references to world.db and screen surface from
 manifest
-Has a controller instance to handle event processing(ui mainly atm)
-Has a pygame clock that measures ms per main game loop
-Has a variable self.run that is True while program is running
"""


class Game:

    def __init__(self,  world_name='Test', start_coordinate_key='0_0_0'):
        pygame.init()
        pygame.mixer.init()
        self.font_init()
        self.platform = sys.platform  # Determine operating system
        self.world = self.world_init(world_name,  start_coordinate_key)
        self.db = self.world.db  # Convenience renaming here
        self.screen = screen
        self.screen_size = screen_size
        self.render_surface_init()
        self.view = self.world_view_init()
        self.controller = Controller(self)
        self.clock = pygame.time.Clock()  # Clock object to tick
        self.tick = self.db['turn_accumulator']  # Load last clock tick value
        self.screen_text_top = []
        self.screen_text = []
        self.selected = None  # Entities left clicked
        self.path_target = None  # Path Finding Target
        self.run = True  # Run while true

    def world_init(self, name='Test', start_coordinate_key='0_0_0'):
        world = World(name)
        if world.db['new_game']:  # If 'new_game'...
            print "NEW GAME"
            # Determine origin_key to activate chunks...
            if world.db['player'] == None:  # If no player yet...
                origin_key = start_coordinate_key  # Use default origin_key
            else:  # Else if player exists...
                origin_key = world.db['player'].coordinate_key
            # Generate a cube shape
            cubeargs = {
                                'origin': key_to_XYZ(origin_key),
                                'magnitude': [32, 32, 1]
                                }
            shape = Cuboid(**cubeargs)
            world.db['view_shape_args'] = cubeargs
            chunks = []
            for coordinate_key in shape.render_key_list:
                parent_chunk = find_parent(coordinate_key)
                if parent_chunk not in chunks:
                    chunks.append(parent_chunk)
                    world.get_chunk(parent_chunk)
            # Generate random base terrain for active chunks
            base = {'image_key': 'grass.png'}
            rocks = {
                            'image_key': 'rocks.png',
                            'speed_modifier': 1.25
                            }
            bushes = {
                            'image_key': 'bush.png',
                            'speed_modifier': 1.50,
                            'layer': 1.1
                            }
            trees = {
                            'image_key': 'tallTree.png',
                            'tall': 20,
                            'float_offset': [0.5, 0.5],
                            'layer': 1.2,
                            'impassible': True,
                            'blocksLOS': True
                            }
            for key in chunks:
                print "##Chunk Building...##", key
                world.chunk_terrain_base_fill(key, **base)
                world.chunk_random_feature_fill(key, **rocks)
                world.chunk_random_feature_fill(key, **bushes)
                world.chunk_random_feature_fill(key, **trees)
            # Initialize player
            if world.db['player'] == None:
                player_args = {
                            'world': world,
                            'coordinate_key': origin_key,
                            'image_key': 'rose.png',
                            'shape': shape,
                            'name': 'Rose'
                           }
                player = Player(**player_args)
                world.add_element(origin_key, player)
                world.db['player'] = player
            world.db['new_game'] = False
        transaction.commit()
        return world

    def render_surface_init(self):
        self.screen_tiles_wide = (self.screen_size[0] / TILE_WIDTH)
        self.screen_tiles_high = (self.screen_size[1] / TILE_HEIGHT)
        self.px_offset = (self.screen_size[0] / 2) - (TILE_WIDTH / 2)
        pixel_y = self.screen_tiles_wide * TILE_HEIGHT
        self.py_offset = (self.screen_size[1] / 2) - (pixel_y / 2)

    def world_view_init(self):
        world = self.world
        args = self.world.db['view_shape_args']
        size = self.screen_size
        px = self.px_offset
        py = self.py_offset
        return WorldView(self.screen, world, args, px, py)

    def font_init(self):
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 16)
        self.font_height = self.font.get_linesize()

    def play_random_song(self):
        try:
            n = random.randint(0, (len(tracks)-1))
            pygame.mixer.music.load(str(tracks[n]))
            pygame.mixer.music.play()
        except pygame.error as Error:
            print "Error: ", Error

    def path(self):
        if self.selected and self.path_target:
            # goal_dict = {self.selected.coordinate_key: 0}
            # sel = self.selected
            # args = self.world.db['view_shape_args']
            # self.selected.path = Path(goal_dict, self.selected, args)
            self.path_target = None

    def reality_bubble_check(self, *elements):
        retire = []
        active_or_adjacent = {}
        for k in world.db['active_chunks']:
            add = find_adjacents(k)
            for k in add:
                active_or_adjacent[k] = None
        for e in elements:
            key = e.coordinate_key
            if key not in active_or_adjacent:
                retire.append(e)
        for e in retire:
            e.deactivate()

    def pixel_collison(self, point, surface, COLORKEY='#0080ff'):
        collide = False
        colorkey = pygame.Color(COLORKEY)
        # Point needs to be adjusted here to have its (x,y) relative
        # to target surface
        if not (surface.get_at(point) == colorkey):
            collide = True
        return collide

    def draw_screen_text(self):
        self.screen_text
        y = self.screen_size[1] - self.font_height
        y2 = 0 + self.font_height
        elements = "Elements = " + str(self.view.e_on_screen)
        self.screen_text.append(elements)
        fps = "FPS = " + str(self.clock.get_fps())
        self.screen_text.append(fps)
        for text in reversed(self.screen_text):
            self.screen.blit(self.font.render(text, True, (255, 0, 0)), (0, y))
            y -= self.font_height
        for text in reversed(self.screen_text_top):
            render = self.font.render(text, True, (255, 0, 0)), (0, y2)
            self.screen.blit(render)
            y2 += self.font_height
        self.screen_text = []

    def ui_surface_init(self):
        pass

    def draw_ui(self):
        horiz_trim_size = ui_manifest['trim.png'].get_size()
        vert_trim_size = ui_manifest['vertical_trim.png'].get_size()
        horiz_trims = screen_size[0]/trim_dimensions[0] + 1
        vert_trims = screen_size[1]/vert_trim_size[1] + 1
        for i in range(horizontal_trims):
            ix = i*trim_dimensions[0]
            py = screen_size[1]-trim_dimensions[1]
            screen.blit(ui_manifest['trim.png'], (ix, 0))
            screen.blit(ui_manifest['trim.png'], (ix, py))
        for i in range(vertical_trims):
            iy = i*vertical_trim_dimensions[1]
            right = screen_size[0] - vertical_trim_dimensions[0]
            screen.blit(ui_manifest['vertical_trim.png'], (0, iy))
            screen.blit(ui_manifest['vertical_trim.png'], (right, iy))

    def db_event(self, key, value):
        self.db[str(key)] = value
        transaction.commit()

    def main_loop(self):
        if not self.run:
            self.world.close()
            sys.exit()
        if self.db['play_music']:
            if not pygame.mixer.music.get_busy():
                self.play_random_song()
        for event in pygame.event.get():
            self.controller.handle_event(event)
        self.path()
        self.world.tick(self.clock.tick())
        self.world.process_effects()
        self.view.render()
        # self.draw_ui()
        self.draw_screen_text()
        pygame.display.flip()

if __name__ == '__main__':
    os.chdir(sys.path[0])
    g = Game()
    while g.run:
        g.main_loop()
    g.world.close()
    sys.exit()
