#!/usr/bin/env python
#######Standard Python Imports#######
import pygame, sys, os
from pygame.locals import *

#Change the CWD to wherever the main.py resides
os.chdir(sys.path[0])

#######Xero Sum Imports#######
from ImageManifests import SCREEN_SIZE, TRACKS, SCREEN
from unboundMethods import *
from World import World
from AoE import *
from WorldView import WorldView
from Chunk import Chunk
from Tile import Tile
from Feature import Feature
from Item import Item
from Entity import Entity
from Field import Field
###########Initilizations####################

####Font Variables###
pygame.font.init()
#AVAILABLE_FONTS = pygame.font.get_fonts() #Not needed atm. Here as a reminder.
FONT = pygame.font.SysFont(None, 16) #None as first param loads built in pygame font
FONT_HEIGHT = FONT.get_linesize()
SCREEN_TEXT = [] #Screen text is a global list that stores the on screen text

###Clock###
TICK  = 0
CLOCK = pygame.time.Clock()

###Game Controls Initialization###
LAST_CLICK = None

####Colors####
WHITE = [255, 255, 255]
BLACK = [0,0,0]
GREEN = [0,255,0]
RED   = [255,0,0]
YELLOW= [255,255,0]