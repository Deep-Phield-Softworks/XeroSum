#!/usr/bin/env python
#Main game script for "Xero Sum"
import random
import os.path
from XeroInit import *
from ImageManifests import *
from Path import Path
from Entity import Entity
from Tile import Tile
###Main Loop###
def mainLoop():
    global TICK
    #Check if music is (not) playing...
    if not pygame.mixer.music.get_busy(): #If no music...
        playRandomSong() #Play a random song
    ###Event Handling###
    for event in pygame.event.get():#Go through all events
        if event.type == QUIT: #If the little x in the window was clicked...
            ensurePersistentData()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                CLICK_HELD = True
            mouseClick(event)
        #if event.type == MOUSEBUTTONUP:
        #    CLICK_HELD = False
        #    mouseClick(event)
        if event.type == KEYDOWN:
            keyboard(event)
        if event.type == KEYUP:
            pass
    
    TICK = CLOCK.tick()
    WORLD.TICK(TICK)
    playerView.render()
    SCREEN.blit(playerView.surface, (0,0))
    drawScreenText() #Draw text onto SCREEN
    pygame.display.flip()      

###KEYBOARD CONTROLS###    
def keyboard(event):
    global SCREEN_TEXT    
    pressed_keys = pygame.key.get_pressed()
    #'ESCAPE' key is for exiting the game
    if pressed_keys[K_ESCAPE]:
        #Save off more safely and unload map
        ensurePersistentData()
        sys.exit()
    #'K_F1' key for screenshot. This saves it to timeString().png
    if pressed_keys[K_F1]:
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H%M%S_%Y-%m-%d')
        filename = timestamp + '.png'
        pygame.image.save((SCREEN),filename)
        print "Screenshot saved as " + filename

#Seperates mouse clicks into left and right and then call their seperate fncs
def mouseClick(event):
    mouse_pos = pygame.mouse.get_pos()
    if (event.button == 1) and (event.type == MOUSEBUTTONDOWN):
        mouseLeftClick(event)
    if (event.button == 1) and (event.type == MOUSEBUTTONUP):
        mouseLeftUp(mouse_pos)
    if event.button == 3 and (event.type == MOUSEBUTTONDOWN):
        mouseRightClick(event)

#This function is called when a left mouse click is passed
def mouseLeftClick(event):
    global SCREEN_TEXT_TOP
    global SELECTED
    SCREEN_TEXT_TOP = []
    point = (event.pos[0],event.pos[1])
    collideList = []
    for e in playerView.hitBoxList:
        if e[0].collidepoint(point):
            if within(e[0], point):
                collideList.append(e)
    for e in collideList:
        info = [e[0],e[1].parentCoordinate, e[1].name, e[1], e[1].floatOffset]
        for bit in info:
            SCREEN_TEXT_TOP.append(str(bit))
        if isinstance(e[1], Entity):
            SELECTED = e[1]

def mouseRightClick(event):
    if SELECTED:
        point = (event.pos[0],event.pos[1])
        goalKeys = []
        for e in playerView.hitBoxList:
            if e[0].collidepoint(point):
                if within(e[0], point):
                    if isinstance(e[1], Tile):
                        goalKeys.append(e[1].parentCoordinate)
                        p = Path(goalKeys, SELECTED, playerView.shape)
                        SELECTED.path = p

#Draw text to the screen.
def drawScreenText():
    global SCREEN_TEXT
    y  = SCREEN_SIZE[1] - FONT_HEIGHT
    y2 = 0 + FONT_HEIGHT
    FPS = "FPS = " + str(CLOCK.get_fps())
    SCREEN_TEXT.append(FPS)
    for text in reversed(SCREEN_TEXT):
        SCREEN.blit( FONT.render(text, True, (255, 0, 0)), (0, y) )
        y -= FONT_HEIGHT
    for text in reversed(SCREEN_TEXT_TOP):
        SCREEN.blit( FONT.render(text, True, (255, 0, 0)), (0, y2) )
        y2 += FONT_HEIGHT
    SCREEN_TEXT = []

#This function is meant to save and close all data in the game.
def ensurePersistentData():
    [WORLD.deactivateChunk(cKey) for cKey in WORLD.active.keys()]
    
#Play a random song
def playRandomSong():
    #Pick a random int between 0 and the length of TRACKS list (-1)
    n = random.randint(0,(len(TRACKS)-1))
    #Load the random song chosen
    pygame.mixer.music.load(str(TRACKS[n]))
    #Play the song once
    pygame.mixer.music.play()

###Test Terrain Gen###
def makeTestTerrain():
    base = ('grass.png', "grass")
    obj  = ('rocks.png', "rocks")
    for key in sorted(WORLD.active.keys()):
        print "##Chunk Building...##", key
        WORLD.baseTerrainChunkFill(key, base)
        WORLD.randomFillChunkFeature(key, obj)
    WORLD.addEntity(WORLD, '10_10_0', 'rose.png', 'Rose')

####TEST WORLD INIT####
WORLD = World("TEST")
origin = [0,0,0]
oKey = makeKey(origin)
shape = Cube(oKey, [21,21,1], True)
#If world db shelf not in existence...
if not os.path.isfile(WORLD.db):##Run Test Terrain Gen
    playerView = WorldView(WORLD, oKey, shape, SCREEN_SIZE)
    makeTestTerrain()
else:#Else just make the playerView
    playerView = WorldView(WORLD, oKey, shape, SCREEN_SIZE)


SELECTED = None
###DEBUG###
print "ACTIVE CHUNKS #:", len(sorted(WORLD.active.keys()))
print "ACTIVE CHUNK IDS:", sorted(WORLD.active.keys())
###DEBUG###
SCREEN_TEXT_TOP = []

while True:
    mainLoop()