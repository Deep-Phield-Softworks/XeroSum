#!/usr/bin/env python
####Font Variables###
import pygame, sys, os, pickle, time, datetime
from pygame.locals import *


###########Initilizations####################
#Change the CWD to wherever the main.py resides
os.chdir(sys.path[0])
pygame.font.init()
#AVAILABLE_FONTS = pygame.font.get_fonts() #Not needed atm. Here as a reminder.
FONT = pygame.font.SysFont(None, 16) #None as first param loads built in pygame font
FONT_HEIGHT = FONT.get_linesize()
SCREEN_TEXT = [] #Screen text is a global list that stores the on screen text

###Clock###
TICK  = 0
CLOCK = pygame.time.Clock()

###Tile Variables###
#For isometric view, tile width should be twice tile height.
TILE_WIDTH   = 64
TILE_HEIGHT  = 32

###Initialize pygame display###
pygame.init()
###Determine Platform###
PLATFORM = sys.platform
SUPPORTED = pygame.display.list_modes() #List of supported resolutions in order from greatest to least
MODES = 0  #Storage variable for all the supportable display modes 
INITIAL_SCREENSIZE = [pygame.display.Info().current_w, pygame.display.Info().current_h]

###Game Controls Initialization###
LAST_CLICK = None

###Config###
CONFIG_EXISTS = False #Value for whether a config exists, presumed false initially
SCROLLABLE = False #Whether screen side mouse scrolling is enable (Disabled for Macs)
config = dict()
if os.path.exists("config.pkl"):
    CONFIG_EXISTS = True
    config = pickle.load( open( "config.pkl", "rb" ) ) 

if not CONFIG_EXISTS: #If no config exists
    SCREEN_SIZE = INITIAL_SCREENSIZE #Set SCREEN_SIZE == first supported resolution
    config['Resolution'] = INITIAL_SCREENSIZE #Update config
    #Assume no bells and whistles graphic support initially
    config['HWSURFACE']  = False
    config['DOUBLEBUF']  = False
    config['SCROLLABLE'] = True
    if pygame.display.mode_ok(SCREEN_SIZE, pygame.FULLSCREEN):
        MODES += pygame.FULLSCREEN
        config['Fullscreen'] = True
    elif pygame.display.mode_ok(SCREEN_SIZE, pygame.RESIZABLE):
        MODES += pygame.RESIZABLE
        config['Fullscreen'] = False
    if pygame.display.mode_ok(SCREEN_SIZE, pygame.HWSURFACE):
        MODES += pygame.HWSURFACE
        config['HWSURFACE'] = True
    if pygame.display.mode_ok(SCREEN_SIZE, pygame.DOUBLEBUF):
        MODES += pygame.DOUBLEBUF
        config['DOUBLEBUF'] = True

    #Using largest supported resolution, determine how many tiles can fit on
    #screen both vertically and horizontally
    screenHeightInTiles = (INITIAL_SCREENSIZE[1] / TILE_HEIGHT)
    screenWidthInTiles  = (INITIAL_SCREENSIZE[0] / TILE_WIDTH)
    if screenHeightInTiles < screenWidthInTiles:
        VIEWPOINT_MAX_SIZE = screenHeightInTiles
    else:
        VIEWPOINT_SIZE = screenWidthInTiles
    config['PLATFORM']       = PLATFORM
    config['TILE_WIDTH']     = TILE_WIDTH
    config['TILE_HEIGHT']    = TILE_HEIGHT
    config['VIEWPOINT_MAX_SIZE'] = VIEWPOINT_MAX_SIZE 
    #Write config to the config file
    pickle.dump( config, open("config.pkl", "wb")) 
    
else: #Else if config.pkl already exists (and was loaded presumably)
    if config['Resolution']: #If key 'Resolution' exists...
        SCREEN_SIZE = config['Resolution'] #That is the screen size
    else: #Otherwise default to largest supported resolution
        SCREEN_SIZE = SUPPORTED[0]
    if config['Fullscreen'] == True:
        MODES += pygame.FULLSCREEN
    elif config['Fullscreen'] == False:
        MODES += pygame.RESIZABLE
    else:
        MODES += pygame.FULLSCREEN
    if config['HWSURFACE'] == True:
        MODES += pygame.HWSURFACE
    if config['DOUBLEBUF'] == True:
        MODES += pygame.DOUBLEBUF
    SCROLLABLE = config['SCROLLABLE']
    
###Initialize Screen###
COLORKEY = pygame.Color('#0080ff')
SCREEN = pygame.display.set_mode(SCREEN_SIZE, MODES)
SCREEN.set_colorkey(COLORKEY)

#Initialize px, py offsets
PXOFFSET = (config['MAP_SURFACE_WIDTH']/2) - (config['TILE_WIDTH']/2)
PYOFFSET = (config['MAP_SURFACE_HEIGHT']/2) + (config['TILE_WIDTH']/2)*3 - (((config['VIEWPOINT_WIDTH'] + 1) * TILE_HEIGHT)/2)
#PYOFFSET = (config['MAP_SURFACE_HEIGHT']/2) - (config['TILE_WIDTH']/2) - (((config['VIEWPOINT_WIDTH'] + 1) * TILE_HEIGHT)/2)

####Colors####
WHITE = [255, 255, 255]
BLACK = [0,0,0]
GREEN = [0,255,0]
RED   = [255,0,0]
YELLOW= [255,255,0]

###Image Initialization###
from spriteSheet import spriteSheet
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
    #Make a SPRITE_MANIFEST entry with filename key and spriteSheet object value
    #spriteSheet objects init variables are:  (imageName, imagepath, framesWide, framesHigh, pixelsWide, pixelsHigh) 
    SPRITE_MANIFEST[str(sprite)] = spriteSheet(sprite, spriteDir, 8, 4)    
    
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

#Initialize the pygame mixer
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
###########Initilizations####################

###########UNBOUND METHODS###################
#Given:  List of ints
#Return: String for use as a dictionary key in form: "x_y_z"
def makeKey(XYZ):
    key = str(XYZ[0])
    for n in XYZ[1:len(XYZ)]:
        key = key + "_" + str(n)
    return key

#Given:  String in form: "int_int_int"
#Return: List of ints
def keyToXYZ(key):
    XYZ = [int(i) for i in key.split('_')]
    return XYZ

#Given: String in form: "int_int_int"
#Return: Parent chunk key string in form: "intX_intY_intZ"
def findParent(coordKey):
    XYZ = keyToXYZ(coordKey)
    parentChunk = makeKey([int(XYZ[0]/16),
                           int(XYZ[1]/16),
                           int(XYZ[2])] )
    return parentChunk

#Given: (x,y) of a mouse click
#Determine if the click is within a tile shaped diamond
def within(rect, point, width = TILE_WIDTH, height = TILE_HEIGHT):
    bool = False
    #4 points that define the rhombus
    A = rect.midleft#(x,(y + (height/2)) )           #9 O'clock
    B = rect.midbottom#((x + (width/2)),(y + height))  #6 O'clock
    C = rect.midright#((x + width),(y + (height/2))) #3 O'clock
    D = rect.midtop#((x + (width/2)),y)             #12 O'clock 

    if (leftOf(A,D,point) > 0):
        if (leftOf(B,C,point) < 0):
            if (leftOf(D,C,point) > 0):
                if (leftOf(A,B,point) < 0):
                    bool = True
    return bool

#Given: 2 points that for a line segment and a third point
#Determine if the third point is:
#-"left and/or above" the line (returns a positive integer),
#-"on the line" (returns 0), or
#-"right and/or below" the line (returns a negative integer)
def leftOf(one, two, point):
    X1 = one[0]
    X2 = two[0]
    Y1 = one[1]
    Y2 = two[1]
    Px = point[0]
    Py = point[1]
    left = (X2 - X1)*(Py - Y1) - (Y2 - Y1)*(Px - X1)
    return left

###########UNBOUND METHODS###################
