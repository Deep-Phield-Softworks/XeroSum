#!/usr/bin/env python
import pygame, pickle, os, math, datetime, sys



###Clock###
TICK = 0
clock = pygame.time.Clock()
###Screen Variables###


COLORKEY = pygame.Color('#0080ff') 

###Screen Variables###
SCREEN_SIZE = (800,600)
ORIGIN = (0,0)

###Maps###
#For isometric view, tile height should be 1/2 of tile width
TILE_WIDTH   = 64
TILE_HEIGHT  = 32
#Each section is 16 tiles wide x 16 tiles tall
#Map surface is 3 sections x 3 sections or 3072x3072 pixels
SECTION_WIDTH = (TILE_WIDTH * 16)
SECTION_HEIGHT = (TILE_HEIGHT * 16)
map_surface_WIDTH = (TILE_WIDTH * 16 * 3) 
map_surface_HEIGHT = (TILE_HEIGHT * 16 * 3)

surface = pygame.Surface((map_surface_WIDTH , map_surface_HEIGHT),32)
surface.set_colorkey(COLORKEY)

from xeroManifest import tileManifest
from xeroManifest import spriteManifest
#The variables Sectors_A through Sectors_D represent 4 points of a diamond shape formed
#from points along the map surface boundaries. Each point is at the midpoint
#of one of the surface edges. A is the midpoint of the leftmost edge. The
#letters go counter-clockwise from there.
Sectors_A = (0, map_surface_HEIGHT/2)
Sectors_B = (map_surface_WIDTH/2, map_surface_HEIGHT)
Sectors_C = (map_surface_WIDTH, map_surface_HEIGHT/2)
Sectors_D = (map_surface_WIDTH/2, 0)

#event_text is the variable that holds text to draw to screen.
event_text = []

###World Init###
worldName = 'testWorld'
worldShelf = 'testWorldShelf'
#Initialize the initial view corner
#corner is a list of [x,y] of top left of a pygame rect. This rect is what is
#shown on the screen.
corner = [(map_surface_WIDTH/2 - SCREEN_SIZE[0]/2),(map_surface_HEIGHT/2 - SCREEN_SIZE[1]/2)]
#Initialize scroll variable. This is used as a global variable to scroll the
#view by changing the values of the corner variable.
scroll = [0,0,0,0]

#Map Bounds. The view corner must stay within these bounds.
boundLeft   = 0 
boundRight  = map_surface_WIDTH - (SCREEN_SIZE[0])
boundTop    = 0 
boundBottom = map_surface_HEIGHT - (SCREEN_SIZE[1])
#The variables A through D represent 4 points of a diamond shape formed
#from points along the map surface boundaries. Each point is at the midpoint
#of one of the surface edges. A is the midpoint of the leftmost edge. The
#letters go counter-clockwise from there.
A = (0, map_surface_HEIGHT/2)
B = (map_surface_WIDTH/2, map_surface_HEIGHT)
C = (map_surface_WIDTH, map_surface_HEIGHT/2)
D = (map_surface_WIDTH/2, 0)
A1B1 = None
A2B2 = None

#Colors as named constants stored in tuples
WHITE = (255,255,255)

###Figures and the UI Variables####
FIGS_SELECTED = []
LAST_CLICK = None
CLICK_HELD = False