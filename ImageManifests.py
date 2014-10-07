#!/usr/bin/env python

#######Standard Python Imports#######
import pygame, sys, os
from unboundMethods import TILE_WIDTH, TILE_HEIGHT
from pygame.locals import *
from SpriteSheet import SpriteSheet
###Initialize pygame display###
pygame.init()
###Determine Platform###
PLATFORM = sys.platform
SUPPORTED = pygame.display.list_modes() #List of supported resolutions in order from greatest to least
MODES = 0  #Storage variable for all the supportable display modes 
SCREEN_SIZE = [pygame.display.Info().current_w, pygame.display.Info().current_h]

SCREEN = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
COLORKEY = pygame.Color('#0080ff')
SCREEN.set_colorkey(COLORKEY)

screenHeightInTiles = (SCREEN_SIZE[1] / TILE_HEIGHT)
screenWidthInTiles  = (SCREEN_SIZE[0] / TILE_WIDTH)
if screenHeightInTiles < screenWidthInTiles:
    VIEWPOINT_MAX_SIZE = screenHeightInTiles
else:
    VIEWPOINT_MAX_SIZE = screenWidthInTiles
#Initialize px, py offsets
PXOFFSET = (SCREEN_SIZE[0]/2) - (TILE_WIDTH/2)
PYOFFSET = (SCREEN_SIZE[1]/2) - ((VIEWPOINT_MAX_SIZE * TILE_HEIGHT)/2)
###Image Initialization###

#This is code is meant to reduce the image loads to the startup only 
#Get the art directories where all the png files reside
artDir    = os.getcwd() + os.sep + "pngs" + os.sep
tileDir   = os.getcwd() + os.sep + "pngs" + os.sep + "tiles"   + os.sep 
spriteDir = os.getcwd() + os.sep + "pngs" + os.sep + "sprites" + os.sep 
TILE_MANIFEST   = dict()
SPRITE_MANIFEST = dict()

for tile in os.listdir(tileDir):
    #Make a TILE_MANIFEST entry with filename key and pygame.image value 
    TILE_MANIFEST[str(tile)] = pygame.image.load(tileDir+tile).convert_alpha()
for sprite in os.listdir(spriteDir):
    #Make a SPRITE_MANIFEST entry with filename key and SpriteSheet object value
    #SpriteSheet objects init variables are:  (imageName, imagepath, framesWide, framesHigh, pixelsWide, pixelsHigh) 
    SPRITE_MANIFEST[str(sprite)] = SpriteSheet(sprite, spriteDir, 8, 4)    
    
###Music Initialization###
#List of tracks for playing a random music
TRACKS = []
#Dictionary of tracks with filenames as keys and filepath as values for playing
#a particular chosen piece
MUSIC_MANIFEST = dict()
musicDir = os.getcwd() + os.sep + "sound" + os.sep + "music" + os.sep
for track in os.listdir(musicDir):
    MUSIC_MANIFEST[str(track)] = str(musicDir) + str(track) #Add track to manifest
    TRACKS.append(str(musicDir) + str(track)) #Add track to random list of songs
###Sound Effects Initialization###
#!!!BROKEN ATM!!!
FX_MANIFEST = dict()
fxDir = os.getcwd() + os.sep + "sound" + os.sep + "FX" + os.sep
for fx in os.listdir(fxDir):
    filename = str(fxDir) + str(track)
    sound = pygame.mixer.Sound(filename)
    FX_MANIFEST[str(fx)] = sound
    
#Initialize the pygame mixer
pygame.mixer.init(frequency=22050, size=-16, channels=4, buffer=4096)
###########Initilizations####################