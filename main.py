#!/usr/bin/env python
#Main game script for "Xero Sum"
import pygame, sys, os, random


from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP,  KEYDOWN,  KEYUP,  K_ESCAPE,  K_F1,  K_F2


from imagemanifests import screen_size, tracks, screen
from world import World
from player import Player
from aoe import *
from worldview import WorldView
from path import Path
from entity import Entity
from tile import Tile
from unboundmethods import make_key, within, timestamp


os.chdir(sys.path[0])
####Font Variables###
pygame.font.init()
#AVAILABLE_FONTS = pygame.font.get_fonts() #Not needed atm. Here as a reminder.
font = pygame.font.SysFont(None, 16) #None as first param loads built in pygame font
font_height = font.get_linesize()
#screen_TEXT & screen_text_top are global string lists that are blit to screen
screen_text = [] 
screen_text_top = []
###Clock###
tick  = 0
clock = pygame.time.Clock()
###Controls Variables###
selected = None #Currently selected Entity

###Main Loop###
def main_loop():
    #Check if music is (not) playing...
    #if not pygame.mixer.music.get_busy(): #If no music...
        #playRandomSong() #Play a random song
    ###Event Handling###
    for event in pygame.event.get():#Go through all events
        if event.type == QUIT: #If the little x in the window was clicked...
            world.close()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            mouse_click(event)
        if event.type == KEYDOWN:
            keyboard(event)
        if event.type == KEYUP:
            pass
    world.tick(clock.tick())
    player_view.render()
    screen.blit(player_view.surface, (0,0))
    draw_screen_text() #Draw text onto screen
    pygame.display.flip()      

###KEYBOARD CONTROLS###    
def keyboard(event):
    global screen_text    
    pressed_keys = pygame.key.get_pressed()
    #'ESCAPE' key is for exiting the game
    if pressed_keys[K_ESCAPE]:
        #Save off more safely and unload map
        world.close()
        sys.exit()
    #'K_F1' key for screenshot. This saves it to timeString().png
    if pressed_keys[K_F1]:
        filename = timestamp() + '.png'
        pygame.image.save((screen),filename)
        print "screenshot saved as " + filename
    if pressed_keys[K_F2]:
        #Hook for the debug
        pass

#Seperates mouse clicks into left and right and then call their seperate fncs
def mouse_click(event):
    mouse_pos = pygame.mouse.get_pos()
    if (event.button == 1) and (event.type == MOUSEBUTTONDOWN):
        mouse_left_click(event)
    if (event.button == 1) and (event.type == MOUSEBUTTONUP):
        pass
        #mouse_left_up(mouse_pos)
    if event.button == 3 and (event.type == MOUSEBUTTONDOWN):
        mouse_right_click(event)

#This function is called when a left mouse click is passed
def mouse_left_click(event):
    global screen_text_top
    global selected
    screen_text_top = []
    point = (event.pos[0],event.pos[1])
    collideList = []
    for e in player_view.hit_box_list:
        if e[0].collide_point(point):
            if within(e[0], point):
                collide_list.append(e)
    for e in collide_list:
        info = [e[1].parent_coordinate, e[1].name, 'float:' + str(e[1].float_offset), 'layer: ' + str(e[1].layer), 'px,py: ', e[1].pixel_offsets]
        screen_text_top.append(str(info))
        if isinstance(e[1], Entity):
            selected = e[1]

def mouse_right_click(event):
    if selected:
        point = (event.pos[0],event.pos[1])
        for e in player_view.hit_box_list:
            if e[0].collide_point(point):
                if within(e[0], point):
                    if isinstance(e[1], Tile):
                        goal_dict = dict()
                        goal_dict[e[1].parent_coordinate] = 0
                        p = Path(goal_dict, selected, Cube(**cubeargs))
                        selected.path = p

#Draw text to the screen.
def draw_screen_text():
    global screen_text
    y  = screen_size[1] - font_height
    y2 = 0 + font_height
    fps = "FPS = " + str(clock.get_fps())
    screen_text.append(fps)
    for text in reversed(screen_text):
        screen.blit( font.render(text, True, (255, 0, 0)), (0, y) )
        y -= font_height
    for text in reversed(screen_text_top):
        screen.blit( font.render(text, True, (255, 0, 0)), (0, y2) )
        y2 += font_height
    screen_text = []

#Play a random song
def playRandomSong():
    #Pick a random int between 0 and the length of tracks list (-1)
    n = random.randint(0,(len(tracks)-1))
    #Load the random song chosen
    pygame.mixer.music.load(str(tracks[n]))
    #Play the song once
    pygame.mixer.music.play()

###Test Terrain Gen###
def makeTestTerrain():
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
    for key in sorted(world.active.keys()):
        print "##Chunk Building...##", key
        world.chunk_terrain_base_fill(key, **base)
        world.chunk_random_feature_fill(key, **rocks)
        world.chunk_random_feature_fill(key, **bushes)
        world.chunk_random_feature_fill(key, **trees)

####TEST world INIT####
world = World("TEST")
origin = [0,0,0]
origin_key = make_key(origin)
cubeargs = {'origin': origin_key, 'magnitude': [10,10,0], 'towards_neg_inf': False}
shape = Cube(**cubeargs)
#If world db shelf not in existence...
if world.db['new_game']:##Run Test Terrain Gen
    player_args = {'world':world,
                             'coordinate_key': origin_key,
                             'image_key':'rose.png',
                             'shape': shape,
                             'name':'Rose'
                           }
    player = Player(**player_args)
    world.add_element(origin_key, player)
    player_view = WorldView(world, shape, screen_size)
    makeTestTerrain()
    world.db['new_game'] = False
else:#Else just make the player_view
    player_view = WorldView(world, shape, screen_size)

###DEBUG###
print "ACTIVE CHUNKS #:", len(sorted(world.db['active_chunks'].keys()))
print "ACTIVE CHUNK IDS:", sorted(world.db['active_chunks'].keys())
###DEBUG###

while True:
    main_loop()
