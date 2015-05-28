#!/usr/bin/env python
import sys
import os
import random


import pygame
import transaction


from controller import Controller
from manifests import screen, screen_size, tracks, fx_manifest, COLORKEY
from world import World
from player import Player
from aoe import *
from worldview import WorldView
from path import Path
from entity import Entity
from tile import Tile
from unboundmethods import key_to_XYZ, find_parent, TILE_WIDTH, TILE_HEIGHT, adjacent

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
        self.tick = self.db['tick_accumulator']  # Load last clock tick value
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
            # Use shape to determine initial actuve chunks
            chunks = []
            # For each coordinate key in shape.area_key_list
            for coordinate_key in shape.render_key_list:
                parent_chunk = find_parent(coordinate_key)
                if parent_chunk not in chunks:  # If not...
                    chunks.append(parent_chunk)  # Add it...
            world.activate_chunk(*chunks)
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
            for key in sorted(world.db['active_chunks'].keys()):
                print "##Chunk Building...##", key
                world.chunk_terrain_base_fill(key, **base)
                world.chunk_random_feature_fill(key, **rocks)
                world.chunk_random_feature_fill(key, **bushes)
                world.chunk_random_feature_fill(key, **trees)
            # Initialize player
            if world.db['player'] == None:
                player_args = {'world':world,
                             'coordinate_key': origin_key,
                             'image_key':'rose.png',
                             'shape': shape,
                             'name':'Rose'
                           }
                player = Player(**player_args)
                world.add_element(origin_key, player)
                world.db['player'] = player
            world.db['new_game'] = False
        transaction.commit()    
        return world 

    def render_surface_init(self):
        self.screen_height_in_tiles = (self.screen_size[1] / TILE_HEIGHT)
        self.screen_width_in_tiles  = (self.screen_size[0] / TILE_WIDTH)
        self.viewpoint_max_size = self.screen_width_in_tiles
        if self.screen_height_in_tiles > self.screen_width_in_tiles:
            self.viewpoint_max_size = self.screen_height_in_tiles
        self.px_offset = (self.screen_size[0]/2) - (TILE_WIDTH/2)
        self.py_offset = (self.screen_size[1]/2) - ((self.viewpoint_max_size * TILE_HEIGHT)/2)
    
    def world_view_init(self):
        #World View Object arguements== WorldView(world, shape, screen_size,  px_offset,  py_offset)
        return WorldView(self.world, self.world.db['view_shape_args'], self.screen_size,  self.px_offset,  self.py_offset)

    def ui_surface_init(self):
        pass
    
    def font_init(self):
        pygame.font.init()
        AVAILABLE_FONTS = pygame.font.get_fonts() #Not needed atm. Here as a reminder.
        self.font = pygame.font.SysFont(None, 16) #None as first param loads built in pygame font
        self.font_height = self.font.get_linesize()

    #Play a random song
    def play_random_song(self):
        #Pick a random int between 0 and the length of tracks list (-1)
        try:
            n = random.randint(0,(len(tracks)-1))
            #Load the random song chosen
            pygame.mixer.music.load(str(tracks[n]))
            #Play the song once
            pygame.mixer.music.play()
        except pygame.error as Error:
            print "Error: ", Error
    
    def path(self):
        if self.selected and  self.path_target:
            #goal_dict = {self.selected.coordinate_key: 0}  #Set target to 0 for DMAP
            #self.selected.path = Path(goal_dict, self.selected, self.world.db['view_shape'])
            self.path_target = None
    
    def reality_bubble_check(self, *elements):
        pass
    
    def pixel_collison(self, point, surface, COLORKEY = '#0080ff'):
        collide = False
        colorkey = pygame.Color(COLORKEY)
        # Point needs to be adjusted here to have its (x,y) relative
        # to target surface
        if not (surface.get_at(point) == colorkey):
            collide = True
        return collide

    def draw_screen_text(self):
        self.screen_text
        y  = self.screen_size[1] - self.font_height
        y2 = 0 + self.font_height
        fps = "FPS = " + str(self.clock.get_fps())
        self.screen_text.append(fps)
        for text in reversed(self.screen_text):
            self.screen.blit(self.font.render(text, True, (255, 0, 0)), (0, y) )
            y -= self.font_height
        for text in reversed(self.screen_text_top):
            self.screen.blit(self.font.render(text, True, (255, 0, 0)), (0, y2) )
            y2 += self.font_height
        self.screen_text = []
    
    def draw_ui(self):
        trim_dimensions = ui_manifest['trim.png'].get_size()
        vertical_trim_dimensions = ui_manifest['vertical_trim.png'].get_size()
        horizontal_trims = screen_size[0]/trim_dimensions[0] + 1
        vertical_trims = screen_size[1]/trim_dimensions[1] + 1
        for i in range(horizontal_trims):
            screen.blit(ui_manifest['trim.png'],(i*trim_dimensions[0],0))
            screen.blit(ui_manifest['trim.png'],(i*trim_dimensions[0], screen_size[1]-trim_dimensions[1]))
        for i in range(vertical_trims):
            screen.blit(ui_manifest['vertical_trim.png'],(0,i*vertical_trim_dimensions[1]))
            screen.blit(ui_manifest['vertical_trim.png'],(screen_size[0] - vertical_trim_dimensions[0], i*vertical_trim_dimensions[1]))

    def db_event(self, key, value):
        self.db[str(key)] = value
        transaction.commit()

    def main_loop(self):
        if not self.run: 
            self.world.close()
            sys.exit()
        if self.db['play_music']: #If music setting in DB..
            if not pygame.mixer.music.get_busy(): #If no music...
                self.play_random_song() #Play a random song
        for event in pygame.event.get(): 
            self.controller.handle_event(event) #Send Events to Controller
        self.path()
        self.world.tick(self.clock.tick())
        self.world.process_effects()
        self.view.render()
        self.screen.blit(self.view.surface, (0,0))
        self.draw_screen_text() #Draw text onto screen
        pygame.display.flip()    

if __name__ == '__main__':
    os.chdir(sys.path[0])
    g = Game()
    while g.run:
        g.main_loop()
    g.world.close()
    sys.exit()
