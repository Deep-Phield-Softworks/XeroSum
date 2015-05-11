#!/usr/bin/env python
import pygame, sys, os

from persistent.mapping import PersistentMapping as pdict

from unboundmethods import TILE_WIDTH, TILE_HEIGHT
from spritesheet import SpriteSheet
###Initialize pygame display###
pygame.init()
###Determine platform###
platform = sys.platform
supported = pygame.display.list_modes() #List of supported resolutions in order from greatest to least
modes = 0  #Storage variable for all the supportable display modes 
screen_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
COLORKEY = pygame.Color('#0080ff')
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
###Image Initialization###

#This is code is meant to reduce the image loads to the startup only 
#Get the art directories where all the png files reside
art_dir    = os.getcwd() + os.sep + "pngs" + os.sep
tile_dir   = os.getcwd() + os.sep + "pngs" + os.sep + "tiles"   + os.sep 
sprite_dir = os.getcwd() + os.sep + "pngs" + os.sep + "sprites" + os.sep 
tile_manifest   = pdict()
sprite_manifest = pdict()

for tile in os.listdir(tile_dir):
    #Make a tile_manifest entry with filename key and pygame.image value   
    if '.png' in str(tile):
        tile_manifest[str(tile)] = pygame.image.load(tile_dir+tile).convert_alpha()
for sprite in os.listdir(sprite_dir):
    #Make a sprite_manifest entry with filename key and SpriteSheet object value
    #SpriteSheet objects init variables are:  (imageName, imagepath, framesWide, framesHigh, pixelsWide, pixelsHigh) 
    if '.png' in str(sprite):
        sprite_manifest[str(sprite)] = SpriteSheet(sprite, sprite_dir, 8, 4)    
    
###Music Initialization###
#List of tracks for playing a random music
tracks = []
#Dictionary of tracks with filenames as keys and filepath as values for playing
#a particular chosen piece
music_manifest = pdict()
music_dir = os.getcwd() + os.sep + "sound" + os.sep + "music" + os.sep
for track in os.listdir(music_dir):
    music_manifest[str(track)] = str(music_dir) + str(track) #Add track to manifest
    tracks.append(str(music_dir) + str(track)) #Add track to random list of songs
###Sound Effects Initialization###
#!!!BROKEN ATM!!!
fx_manifest = pdict()
fx_dir = os.getcwd() + os.sep + "sound" + os.sep + "FX" + os.sep
for fx in os.listdir(fx_dir):
    filename = str(fx_dir) + str(track)
    sound = pygame.mixer.Sound(filename)
    fx_manifest[str(fx)] = sound
    
#Initialize the pygame mixer
pygame.mixer.init(frequency=22050, size=-16, channels=8, buffer=4096)
###########Initilizations####################
