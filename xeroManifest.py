#!/usr/bin/env python
import pygame, os
from xeroConstants import *
from image import image

#This is a module meant to reduce the image loads to the startup only 

###!!!WARNING!!!###
#If you see:
#"pygame.error: cannot convert without pygame.display initialized"
#move the xeroManifest import statement to after the pygame screen
#is initialized

#Get the art directory where all the png files reside
artdir = os.getcwd() + os.sep + "pngs" + os.sep

#######TILES###############
#Open the tile manifest text. The file names in the manifest will be used
#to generate the tile image dictionary.
tileFile = open('tileManifest.txt', 'r')
#Make a list of tile file names
tiles = tileFile.readlines()
#Scrub any newline characters
c = 0
for tile in tiles:
    split = tile.split('\n')
    tiles[c] = split[0]
    c+=1
#Create a dictionary for the tile images
tileManifest = dict()
#For each tile in the list...
for tile in tiles:
    #Make a dictionary entry with the filename as the key and the pygame.image
    #as the value
    tileManifest[str(tile)] = pygame.image.load(artdir+tile).convert_alpha()

#######SPRITES/FIGURES###########
#Create a dictionary for the sprite images
spriteManifest = dict()
spriteFile = open('spriteManifest.txt', 'r')
#Make a list of sprite file names
sprites = spriteFile.readlines()
#Scrub any newline characters
c = 0
for sprite in sprites:
    split = sprite.split('\n')
    sprites[c] = split[0]
    c+=1
for sprite in sprites:
    #Make a dictionary entry with the filename as the key and the pygame.image
    #as the value
    spriteManifest[str(sprite)] = image(sprite,8,4,256,256)