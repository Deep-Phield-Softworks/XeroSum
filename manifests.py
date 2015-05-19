#!/usr/bin/env python
import os


import pygame


from unboundmethods import TILE_WIDTH, TILE_HEIGHT
from spritesheet import SpriteSheet
from itemsheet import ItemSheet


#Initialize main screen to provide surface for image manifests to be initialized
pygame.init()
screen_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
COLORKEY = pygame.Color('#0080ff')
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
screen.set_colorkey(COLORKEY)

###Image Initialization###
#This is code is meant to reduce the image loads to the startup only 
#Get the art directories where all the png files reside
art_dir      = os.path.join(os.getcwd(), 'pngs')
tile_dir     = os.path.join(art_dir, 'tiles')
item_dir   = os.path.join(art_dir, 'items')
sprite_dir = os.path.join(art_dir, 'sprites')
ui_dir       = os.path.join(art_dir, 'ui')
tile_manifest     = dict()
sprite_manifest = dict()
item_manifest   = dict()
ui_manifest   = dict()

for tile in os.listdir(tile_dir):
    #Make a tile_manifest entry with filename key and pygame.image value   
    if '.png' in str(tile):
        path = os.path.join(tile_dir, tile)
        tile_manifest[str(tile)] = pygame.image.load(path).convert_alpha()
for sprite in os.listdir(sprite_dir):
    #Make a sprite_manifest entry with filename key and SpriteSheet object value
    #SpriteSheet objects init variables are:  (imageName, imagepath, framesWide, framesHigh, pixelsWide, pixelsHigh) 
    if '.png' in str(sprite):
        path = os.path.join(sprite_dir, sprite)
        sprite_manifest[str(sprite)] = SpriteSheet(sprite, path, 8, 4) 
for item_sheet in os.listdir(item_dir):
    #Make a item_manifest entry with filename key and pygame.image object value
    if '.png' in str(item_sheet):
        path = os.path.join(item_dir, item_sheet)
        item_manifest[str(item_sheet)] = ItemSheet(item_sheet,  path)
for ui_img in os.listdir(ui_dir):
    #Make a ui_manifest entry with filename key and pygame.image value   
    if '.png' in str(ui_img):
        path = os.path.join(ui_dir, ui_img)
        ui_manifest[str(ui_img)] = pygame.image.load(path)
    
###Music Initialization###
pygame.mixer.init()
#List of tracks for playing music
tracks = []
#Dictionary of tracks with filenames as keys and filepath as values for playing
#a particular chosen piece
music_manifest = dict()
music_dir = os.getcwd() + os.sep + "sound" + os.sep + "music" + os.sep
for track in os.listdir(music_dir):
    music_manifest[str(track)] = str(music_dir) + str(track) #Add track to manifest
    tracks.append(str(music_dir) + str(track)) #Add track to random list of songs

###Sound Effects Initialization###
fx_manifest = dict()
fx_dir = os.getcwd() + os.sep + "sound" + os.sep + "FX" + os.sep
for fx in os.listdir(fx_dir):
    filename = str(fx_dir) + str(fx)
    sound = pygame.mixer.Sound(filename)
    key = fx.split('.')[0] #Split filename on '.' and keep first half for use as fx_manifest dict key
    fx_manifest[str(key)] = sound
    
