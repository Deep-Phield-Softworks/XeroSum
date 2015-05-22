#!/usr/bin/env python
#Main game script for "Xero Sum"
import pygame, sys, os, random


import transaction
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP,  KEYDOWN,  KEYUP,  K_ESCAPE,  K_F1,  K_F2,  K_F3


from manifests import tracks, fx_manifest, ui_manifest
from world import World
from player import Player
from aoe import *
from worldview import WorldView
from path import Path
from entity import Entity
from tile import Tile
from unboundmethods import make_key, within, timestamp,  TILE_WIDTH,  TILE_HEIGHT

###Initialize pygame display###
pygame.init()

platform = sys.platform
screen_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
COLORKEY = pygame.Color('#0080ff')
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
screen.set_colorkey(COLORKEY)

screen_height_in_tiles = (screen_size[1] / TILE_HEIGHT)
screen_width_in_tiles  = (screen_size[0] / TILE_WIDTH)
if screen_height_in_tiles < screen_width_in_tiles:
    viewpoint_max_size = screen_height_in_tiles
else:
    viewpoint_max_size = screen_width_in_tiles
#Initialize px, py offsets
px_offset = (screen_size[0]/2) - (TILE_WIDTH/2)
py_offset = (screen_size[1]/2) - ((viewpoint_max_size * TILE_HEIGHT)/2)
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
    if world.db['play_music']:
        if not pygame.mixer.music.get_busy(): #If no music...
            play_random_song() #Play a random song
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
    #draw_ui()
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
    #'K_F1' key to toggle music
    if pressed_keys[K_F1]:
        pygame.mixer.music.stop()
        world.db['play_music'] = not world.db['play_music']
        transaction.commit()
    #'K_F2' key for screenshot. This saves it to timeString().png    
    if pressed_keys[K_F2]:
        filename = timestamp() + '.png'
        pygame.image.save((screen),filename)
        print "screenshot saved as " + filename
    if pressed_keys[K_F3]:
        #Play random sound
        fx_manifest[random.choice(fx_manifest.keys())].play()

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
    collide_list = []
    selected = None
    selected_info = None
    for e in player_view.hit_box_list:
        if e[0].collidepoint(point):
            if within(e[0], point):
                collide_list.append(e)
    if collide_list:
        for e in collide_list:
            info = [e[1].coordinate_key, e[1].name, 'float:' + str(e[1].float_offset), 'layer: ' + str(e[1].layer), 'px,py: ', e[1].pixel_offsets]
            screen_text_top.append(str(info))
            if isinstance(e[1], Entity):
                selected = e[1]
                selected_info = info

def mouse_right_click(event):
    if selected:
        point = (event.pos[0],event.pos[1])
        for e in player_view.hit_box_list:
            if e[0].collidepoint(point):
                if within(e[0], point):
                    if isinstance(e[1], Tile):
                        goal_dict = dict()
                        goal_dict[e[1].coordinate_key] = 0
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
def play_random_song():
    #Pick a random int between 0 and the length of tracks list (-1)
    try:
        n = random.randint(0,(len(tracks)-1))
        #Load the random song chosen
        pygame.mixer.music.load(str(tracks[n]))
        #Play the song once
        pygame.mixer.music.play()
    except pygame.error as Error:
        print "Error: ", Error

def draw_ui():
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
    for key in sorted(world.db['active_chunks'].keys()):
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
                             'name':'Rose'
                           }
    player = Player(**player_args)
    world.add_element(origin_key, player)
    makeTestTerrain()
    world.db['new_game'] = False

player_view = WorldView(world, shape, screen_size,  px_offset,  py_offset)

###DEBUG###
print "ACTIVE CHUNKS #:", len(sorted(world.db['active_chunks'].keys()))
print "ACTIVE CHUNK IDS:", sorted(world.db['active_chunks'].keys())
###DEBUG###

while True:
    main_loop()
