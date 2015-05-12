#!/usr/bin/env python
import pygame, sys, os, random


import transaction

from manifests import screen_size, tracks, screen,  fx_manifest
from world import World
from player import Player
from aoe import *
from worldview import WorldView
from path import Path
from entity import Entity
from tile import Tile
from unboundmethods import find_parent

#Game Class for Xero Sum
#Game is a high level wrapper that has the following attributes:
#-Has clock object

class Game:
    def __init__(self,  world_name = 'Test',  player_start_coordinate_key = '0_0_0'):
        self.clock = pygame.time.Clock()
        self.world = self.world_init(world_name,  player_start_coordinate_key)
        self.db = self.world.db #Convenience renaming here 
        self.tick  = self.db['tick_accumulator']
        #self.player_view = WorldView(world, shape, screen_size)
        
    def world_init(self,  name = 'Test',  player_start_coordinate_key = '0_0_0'):
        world = World(name)
        if world.db['new_game']: #If 'new_game'...
            #Determine origin_key to activate chunks...
            if world.db['player'] == None: #If no player yet...
                origin_key = player_start_coordinate_key #Use given/default coordinates for origin_key
            else:                                              #Else if player exists...
                origin_key =world.db['player'].coordinate_key #Use their coordinate_key
            #Generate a cube shape
            cubeargs = {'origin': origin_key, 'magnitude': [10,10,0], 'towards_neg_inf': False} 
            shape = Cube(**cubeargs)
            world.db['view_shape'] = shape #Store shape for later use in self.player_view
            #Use shape to determine initial actuve chunks
            chunks = []
            #For each coordinate key in shape.area_key_list
            for coordinate_key in shape.area_key_list:
                parent_chunk = find_parent(coordinate_key)
                if parent_chunk not in chunks: #If not...
                    chunks.append(parent_chunk)  #Add it...
            world.activate_chunk(*chunks)
            #Generate random base terrain for active chunks
            base = {'image_key': 'grass.png'}
            #feature(image_key, name = None, speed_modifier = 1.0, tall = 0, float_offset = [0.5,0.5], impassible = False, blocksLOS = False)
            rocks = {'image_key':'rocks.png', 'speed_modifier': 1.25, 'layer': 1.0}
            bushes = {'image_key': 'bush.png', 'speed_modifier': 1.50, 'layer': 1.1}
            trees  = {'image_key': 'tallTree.png', 
                            'tall': 20,
                            'float_offset': [0.5, 0.5],
                            'layer': 1.2,
                            'impassible': True,
                            'blocksLOS': True }
            for key in sorted(world.db['active_chunks'].keys()):
                print "##Chunk Building...##", key
                world.chunk_terrain_base_fill(key, **base)
                world.chunk_random_feature_fill(key, **rocks)
                world.chunk_random_feature_fill(key, **bushes)
                world.chunk_random_feature_fill(key, **trees)
            #Initialize player
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

if __name__ == '__main__':
    g = Game()
