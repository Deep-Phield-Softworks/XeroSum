#!/usr/bin/env python
#Main game script for "Xero Sum"

###Imports###
import pygame, sys
from pygame.locals import * #Import common pygame variables (FULLSCREEN,etc)
###Initialize###
pygame.init()
SUPPORTED = pygame.display.list_modes()
FLAGS = 0
if pygame.display.mode_ok(SUPPORTED[0],pygame.FULLSCREEN):
    FLAGS += pygame.FULLSCREEN
else:
    FLAGS += pygame.RESIZABLE
if pygame.display.mode_ok(SUPPORTED[0],pygame.HWSURFACE):
    FLAGS += pygame.HWSURFACE
if pygame.display.mode_ok(SUPPORTED[0],pygame.DOUBLEBUF):
    FLAGS += pygame.DOUBLEBUF
SCREEN_SIZE = SUPPORTED[0]
screen = pygame.display.set_mode(SCREEN_SIZE, FLAGS)

#Xero Sum Imports
from xeroConstants import *
import libraryXero as lib
from tile import tile
from section import section
from world import world
from path import path
from figure import figure


###Font Variables###
font = pygame.font.SysFont("arial",16)
font_height = font.get_linesize()
event_text = []
###Maps###


###World Init###
w = world(worldName, worldShelf)
w.loadCurrentSections(lib.dbKeyStringToXY(w.currentCenter))
w.figures = []

w.genFigure(0,0,w.currentCenter, spriteManifest['rose.png'])
w.genFigure(2,2,w.currentCenter, spriteManifest['rose.png'])
w.genFigure(8,4,w.currentCenter, spriteManifest['rose.png'])
w.genFigure(7,3,w.currentCenter, spriteManifest['rose.png'])
w.genFigure(1,1,w.currentCenter, spriteManifest['rose.png'])
w.genFigure(4,2,w.currentCenter, spriteManifest['rose.png'])

###Main Loop###
def mainLoop():
    global corner 
    global scroll
    global TICK
    global CLICK_HELD
    TICK = clock.tick()
    ###Event Handling###
    for event in pygame.event.get():#Go through all events
        if event.type == QUIT: #If the little x in the window was clicked...
            #Save off more safely and unload map
            w.unloadOldSections(w.currentSections)
            sys.exit()
        if event.type == MOUSEMOTION: 
            scroll = mouseMove(event)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                CLICK_HELD = True
            mouseClick(event)
        if event.type == MOUSEBUTTONUP:
            CLICK_HELD = False
            mouseClick(event)
        if CLICK_HELD:
            mouse_pos = pygame.mouse.get_pos()
            mouseLeftUp(mouse_pos)
        if event.type == KEYDOWN:
            key(event) #Remove return when mouse move imp'd
        if event.type == KEYUP:
            scroll = [0,0,0,0]
    
    ###Rendering###
    #Map Render
    w.render(TICK, surface)
    #corner is the [x,y] of the top left of the view Rect
    corner = lib.checkBoundaries(corner) #Keep view in Bounded area
    inside = w.viewInBoundsCheck()
    #view is a smaller screen-sized piece of the bigger map. 
    view = Rect(corner[0],corner[1],SCREEN_SIZE[0],SCREEN_SIZE[1])
    screen.blit(surface.subsurface(view), (0,0))
    #Draw FPS and debug text
    drawScreenText()
    
    time_passed = TICK * 2
    #Scroll view based on time passed and edges touched by mouse
    if (inside):
        scrollView(scroll, time_passed)
    #pygame.display.update()
    pygame.display.flip()
    

#Given: an (x,y) of a mouse click
#Determine what section was clicked and return that section
def whatSection(click):
    clicked = None
    for sect in w.currentSections:
        if (sect.withinSection(click)):
            clicked = sect
            return clicked
    return clicked

#Given: (x,y) of a mouse click
#Determine what tile was clicked and return tile Str(x,y,z) 
def findTileClicked(point):
    sect = whatSection(point)
    c = 0
    tile = None
    max = (len(sect.spool)/4) - 1
    mid = len(sect.spool)/2
    while (c <= max) and (tile == None):
        t = sect.spool[(0 + c)]
        if t.withinTile(point):
            tile = sect.spool[(0 + c)]
        t = sect.spool[(255 - c)]
        if t.withinTile(point):
            tile = sect.spool[(255 - c)]
        t = sect.spool[((mid -1) - c)]
        if t.withinTile(point):
            tile = sect.spool[((mid -1) - c)]
        t = sect.spool[(mid + c)]
        if t.withinTile(point):
            tile = sect.spool[(mid + c)]
        c += 1
    if tile == None:
        tile = (None, None, None)
    else:
        tile = tile.tileMapID()
    
    return tile

#Draw text to the screen.
def drawScreenText():
    y = SCREEN_SIZE[1]-font_height
    for text in reversed(event_text):
        screen.blit( font.render(text, True, (255, 0, 0)), (0, y) )
        y-=font_height
    FPS = "FPS = " + str(clock.get_fps())
    screen.blit( font.render(FPS, True, (255, 0, 0)), (0, 0) )
    

#Scroll the view subsurface based on which side of the screen is being moused
def scrollView(scroll, time_passed):
    #Calculate corner from mouse position
    #Left of screen is being touched
    if scroll[0] == 1:
        corner[0] = corner[0] - int(time_passed/2)
    #Right of screen is being touched
    if scroll[1] == 1:
        corner[0] = corner[0] + int(time_passed/2)
    #Top of screen is being touched
    if scroll[2] == 1:
        corner[1] = corner[1] - int(time_passed/2)
    #Bottom of screen is being touched
    if scroll[3] == 1:
        corner[1] = corner[1] + int(time_passed/2)

#The mouseMove function takes an event of type MOUSEMOVE
def mouseMove(event):
    pos = event.pos #pos is a tuple with (x,y) mouse position
    scroll = [0,0,0,0] #List that returns edges of the screen mouse is touching
    if pos[0] == 0: #Left Side (x == 0)
        scroll[0] = 1 #Scroll Left 
    if pos[0] == (SCREEN_SIZE[0]-1): #The SCREEN_SIZE[0] minus 1 == correct right-most value
        scroll[1] = 1 #Scroll Right 
    if pos[1] == 0: #Top Side (y == 0)
        scroll[2] = 1 #Scroll Up
    if pos[1] == (SCREEN_SIZE[1]-1): #The SCREEN_SIZE[1] minus 1 == correct bottom-most value
        scroll[3] = 1 #Scroll Down
    return scroll

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
    global event_text
    global LAST_CLICK
    global FIGS_SELECTED
    FIGS_SELECTED = []
    point = (event.pos[0] + corner[0],event.pos[1] + corner[1])
    #contents[] is strings to print as Debug info
    contents = []
    #contents = event_text #For Persistent Text Uncomment this line 
    section = whatSection(point)
    #point[] == Pixel coordinates of mouse click
    #point[] must be have the corner offset added
    contents.append(str(point))
    
    if section != None:
        contents.append(section.name)
        tile = findTileClicked(point)
        contents.append(str(tile))
    else:
        contents.append("No Section")
    event_text = contents
    LAST_CLICK = point
    if not None in tile:
        for entry in section.MAP[tile[0]][tile[1]]:
            if isinstance(entry, figure):
                FIGS_SELECTED.append(entry)
    #print str(FIGS_SELECTED)

#This function is called when a left mouse button is up
def mouseLeftUp(mouse_pos):
    global event_text
    global LAST_CLICK
    #event_text = []

    point = (mouse_pos[0] + corner[0],mouse_pos[1] + corner[1])
    if point != LAST_CLICK:
        deltaX = point[0] - LAST_CLICK[0]
        deltaY = point[1] - LAST_CLICK[1]
        p3 = [(LAST_CLICK[0] + deltaX), LAST_CLICK[1]]
        p4 = [LAST_CLICK[0], (LAST_CLICK[1] + deltaY)]
        color = (0,255,0)
        pygame.draw.line(surface, color, LAST_CLICK, p3)
        pygame.draw.line(surface, color, LAST_CLICK, p4)
        pygame.draw.line(surface, color, point, p3)
        pygame.draw.line(surface, color, point, p4)
    
def mouseRightClick(event):
    global event_text
    global FIGS_SELECTED
    event_text = []
    mouse_pos = pygame.mouse.get_pos()
    point = (mouse_pos[0] + corner[0],mouse_pos[1] + corner[1])
    section = whatSection(point)
    if section != None:
        tile = findTileClicked(point)
        if not None in tile:
            tile = section.MAP[tile[0]][tile[1]][0]
            for fig in FIGS_SELECTED:
                initial = [fig.section, fig.MAPX, fig.MAPY]
                center = w.currentCenter
                goals = [[section.name,tile.MAPX,tile.MAPY]]
                fig.path = path(initial, center, goals)
    
###KEYBOARD CONTROLS###    
def key(event):
    pressed_keys = pygame.key.get_pressed()
    #'ESCAPE' key is for exiting the game
    if pressed_keys[K_ESCAPE]:
        #Save off more safely and unload map
        w.unloadOldSections(w.currentSections)
        sys.exit()
    #'s' key is for screenshot. This saves it to timeString().png
    if pressed_keys[K_s]:
        filename = lib.timeString() + '.png'
        pygame.image.save((surface.subsurface(view)),filename)
        print "Screenshot saved as " + filename
    
    #MOVEMENT KEYS
    if pressed_keys[K_LEFT]:
        scroll[0] = 1 #Scroll Left
    elif pressed_keys[K_RIGHT]:
        scroll[1] = 1 #Scroll Right 
    if pressed_keys[K_UP]:
        scroll[2] = 1 #Scroll Up
    elif pressed_keys[K_DOWN]:
        scroll[3] = 1 #Scroll Down

while True:
    mainLoop()
