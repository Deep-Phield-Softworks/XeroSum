#!/usr/bin/env python
import pickle, os, shelve
from section import section
from figure import figure
from path import path
import libraryXero as lib
from xeroConstants import *
from tile import tile

#World class manages the section db.
#Sections keys in db take the form of: "sect_x_y"

class world:
    def __init__(self, name, shelfName, TILE_WIDTH = 64, TILE_HEIGHT  = 32):
        self.name = name
        self.shelfName = shelfName
        self.currentSections = []
        self.currentSectionsDict = dict()
        self.currentCenter = "sect_1_1"
        self.TILE_WIDTH = TILE_WIDTH
        self.TILE_HEIGHT = TILE_HEIGHT
        self.WIDTH = (self.TILE_WIDTH * 16 * 3)
        self.HEIGHT = (self.TILE_HEIGHT * 16 * 3)
        self.figures = []
    
    def getFigsSelected(self, click):
        pass
    
    def render(self, TICK, surface):
        #This first section.render() takes care of freshly loaded sectors 
        [sect.render(TICK, surface) for sect in self.currentSections]
        
        #For each figure, blit their background surface to create a blank slate 
        for fig in self.figures: #For each figure...
            if fig.section in self.currentSectionsDict: #If fig in a section in scope..
                    fig.renderBack(surface) 
        #Move the figures    
        for fig in self.figures:
            #First store their old sector coordinates
            old = [fig.section, fig.MAPX, fig.MAPY]
            #Now get their "new" coordinates
            next = fig.move(TICK)
            #If the coordinates of the figure have changed...
            if next != old:
                #Remove the figure from it's old sect.MAP entry 
                if old[0] in self.currentSectionsDict:
                    self.currentSectionsDict[old[0]].MAP[old[1]][old[2]].remove(fig)
                #Add the figure to it's next sect.MAP entry
                if next[0] in self.currentSectionsDict:
                    self.currentSectionsDict[next[0]].MAP[next[1]][next[2]].append(fig)
            #For each figure, calculate their next px,py position and store
            #that as their new background surface
            if fig.section in self.currentSectionsDict:
                #Adjust the figure's px,py
                px = self.currentSectionsDict[fig.section].MAP[fig.MAPX][fig.MAPY][0].px
                py = self.currentSectionsDict[fig.section].MAP[fig.MAPX][fig.MAPY][0].py
                figX = px - (fig.width/2) + (TILE_WIDTH/2)
                figY = py - fig.height + (TILE_HEIGHT/2)
                fig.setPos(figX,figY)
                #While slate is blank, get new Background
                fig.getBack(surface)
        #This is the "main" part of the render.
        #For each section in the ordered list of current sections...
        for sect in self.currentSections:
            for MAPY in range(sect.MAP_HEIGHT):
                for MAPX in range(sect.MAP_WIDTH): #For "MAPZ"...
                    z = sect.MAP[MAPX][MAPY]
                    hasFigure = False
                    #For item in "MAPZ"...
                    for item in z: 
                        if isinstance(item,figure):
                            hasFigure = True
                        else: #If hasFigure == False
                            if item.tall: #If a tile is tall...
                                item.render(TICK, surface) #Render it to prevent truncation
                    if hasFigure: 
                        #Render everything at first, tiles and the figure
                        for item in z:
                            item.render(TICK, surface)
                        for item in z: #Then render again...
                            if isinstance(item, tile):    #The tiles...
                                if item.tall or item.conceals: #That are tall or conceal
                                    item.render(TICK, surface)
                
    #Method to generate a figure and add it to the figures list to be rendered    
    def genFigure(self,  MAPX, MAPY, section, image):
        if section in  self.currentSectionsDict:
            #Calculate figure px, py
            px = self.currentSectionsDict[section].MAP[MAPX][MAPY][0].px
            py = self.currentSectionsDict[section].MAP[MAPX][MAPY][0].py
                    
            #Add a figure as the last entry of world.figures
            fig = figure(MAPX, MAPY, section, image,px,py, len(self.figures))
            figX = px - (fig.width/2) + (TILE_WIDTH/2)
            figY = py - fig.height + (TILE_HEIGHT/2)
            fig.setPos(figX,figY)
            self.figures.append(fig)
            #Reassign section to hold the object and not the DB key string
            #Lastly, add the figure to the section MAP data           
            self.currentSectionsDict[section].MAP[MAPX][MAPY].append(self.figures[-1])
        
    #Given: Screen View Top-Left Corner
    #Determine if view's four corners are in-bounds of the nine sections.
    def viewInBoundsCheck(self):
        inside = True
        centerModifier = [0,0]
        #This variable represents the four corners of the screen view
        fourCorners = (
            (corner[0],corner[1]),
            (corner[0] + SCREEN_SIZE[0],corner[1]),
            (corner[0],corner[1] + SCREEN_SIZE[1]),
            (corner[0] + SCREEN_SIZE[0],corner[1]+ SCREEN_SIZE[1])
                       )
        #Top Left Corner Outside
        if (lib.leftOf(A,D,fourCorners[0]) < 0):
            inside = False
            centerModifier[0] += -1 # next center x - 1
        #Bottom Left Corner Outside
        if (lib.leftOf(A,B, fourCorners[2]) > 0):
            inside = False
            centerModifier[1] += 1 # next center y + 1
        #Bottom Right Corner Outside 
        if (lib.leftOf(B,C,fourCorners[3]) > 0):
            inside = False
            centerModifier[0] += 1 # next center x + 1
        #Top Right Corner Outside    
        if (lib.leftOf(C,D,fourCorners[1]) > 0):
            inside = False
            centerModifier[1] += - 1 # next center y - 1
        #If not inside, it's time to change the current center section
        if not inside:
            #Store the screen view to maintain the illusion of continuity
            A1B1 = self.defineViewPoints(centerModifier[0],centerModifier[1])    
            A2B2 = self.defineViewPoints(0,0)
            #The absolute values of (x1 - x2) and (y1-y2) are the offset distance
            #Find the absolute value of the difference between the x values of Point A1 and B1
            absX = abs(A1B1[0][0] - A1B1[1][0])
            #Find the absolute value of the difference between the y values of Point A1 and B1
            absY = abs(A1B1[0][1] - A1B1[1][1])
            B2 = A2B2[1] #B2 is the new location of the reference point 
            posMods = self.relationalPosition(A1B1)
            self.moveCenter(centerModifier)
            corner[0] = B2[0] + (absX * posMods[0])
            corner[1] = B2[1] + (absY * posMods[1])
            
        return inside
    
    def moveCenter(self, centerModifier):
        center = self.currentCenter #Get dbKeyString of old center
        centerCoord = lib.dbKeyStringToXY(center) #Change to coordinates
        #Calculate next Center (x,y) from screen view corners out of bounds
        nextCenter = [(centerCoord[0] + centerModifier[0]),(centerCoord[1] + centerModifier[1])]
        #Make coordinates into db key string
        center = lib.dbKeyString(nextCenter[0],nextCenter[1])
        #Change the center to new center
        self.currentCenter = center
        self.loadCurrentSections((nextCenter))
    
    #Load current sections given the (x,y) of center section
    def loadCurrentSections(self, (next_x, next_y)):
        x = next_x
        y = next_y
        oldSections = self.currentSections
        #This step loads the current sections as db keys into self.currentSections
        self.currentSections = self.calcCurrentSections(x,y)
        
        self.unloadOldSections(oldSections)
            
        #Load section objects into each slot, overwriting the db key string
        c = 0
        for key in self.currentSections:
            self.currentSections[c] = self.loadSection(key)
            c += 1
        #Empty section name dictionary
        self.currentSectionsDict = dict()
        #Populate the dict with the current sections
        for sect in self.currentSections:
            self.currentSectionsDict[sect.name] = sect
    
        #For each section, offset each tile in that section
        c = 0
        for sect_y in range(3):
            for sect_x in range(3):
                self.currentSections[c].offsetTiles(self.sectionScreenOffset(sect_x, sect_y))
                c += 1
  
    #Load an existing section and return it
    #If section doesn't yet exist, then make it and return it
    #Parameters: tuple (x,y) == absolute coordinates of the section
    #            tuple (iso_px,iso_py) == one of the nine on screen sections  
    def loadSection(self, key):
        db = shelve.open(self.shelfName)
        if db.has_key(key):
            section = db[key]
        else:
            section = self.makeSection(key)
            db[key] = section
        db.close()
        section.loadImages(tileManifest)
        section.dirtyAll()
        for fig in self.figures:
            if fig.section == key:
                section.MAP[fig.MAPX][fig.MAPY].append(fig)
        return section
    
    
    #Helper method for viewInBoundsCheck
    #Return the screen view corner (Point A) as a point and a reference
    #point (Point B). The reference point B will be the top point of the center
    #section. This is defined (roughly) as it's (MAP[0][0][0].x,MAP[0][0][0].y)
    def defineViewPoints(self, x, y):
        if x == -1 and y == -1: #North
            sect = self.currentSections[0]
        if x == 0 and y == -1: #NE
            sect = self.currentSections[1]
        if x == 1 and y == -1: #East
            sect = self.currentSections[2]
        if x == -1 and y == 0: #NW
            sect = self.currentSections[3]
        if x == 0 and y == 0: #Center
            sect = self.currentSections[4]
        if x == 1 and y == 0: #SE
            sect = self.currentSections[5]
        if x == -1 and y == 1: #West
            sect = self.currentSections[6]
        if x == 0 and y == 1: #SW
            sect = self.currentSections[7]
        if x == 1 and y == 1: #South
            sect = self.currentSections[8]
        
        A1 = (corner[0], corner[1])    
        B1 = (sect.MAP[0][0][0].px, sect.MAP[0][0][0].py)
        return [A1, B1]
        
    
        
    #Helper method for viewInBoundsCheck
    #Given: a pair of points in (x,y) format
    #Return the first point's location along the x,y axes in relation to second
    #point as signed integer in format (x realtive, y relative)  
    def relationalPosition(self, points):
        A = points[0]
        B = points[1]
        if   A[0] <  B[0]:
            x = -1
        else:
            x = 1
        if   A[1] <  B[1]:
            y = -1
        else:
            y = 1
        return (x,y)
    
    
    #Save off all the old sections
    def unloadOldSections(self, sections):
        for old in sections:
            self.unloadSection(old)
            
    #Save off section and unload it
    def unloadSection(self, section):
        db = shelve.open(self.shelfName)
        key = section.name
        for fig in self.figures:
            if fig.section == key:
                MAPX = fig.MAPX
                MAPY = fig.MAPY
                #This step seems redundant but the interpreter was throwing
                #errors without it...so idk
                if fig in section.MAP[MAPX][MAPY]:
                    section.MAP[MAPX][MAPY].remove(fig)
        section.unloadImages()
        db[key] = section
        db.close()
        
    #Make a new section and return it.
    #Parameters: DB key, where key == str(sect_x_y)
    def makeSection(self, key):
        sect = section(key)
        sect.makeBaseLayer() #Make bottom layer
        sect.spoolTiles()    #"Spool" base layer tiles into easily iterated form
        #Create random layers
        #randomLayer(image, chance, conceals = True, tall = False, tallMod = 32)
        sect.randomLayer(('rocks.png'), 8, False)
        sect.randomLayer(('bush.png'), 8, True)
        sect.randomLayer(('tallTree.png'), 12, True, True)
        return sect

    #Given: Current Center Section's (x,y)
    #Return: List composed of center and adjacent sections in db[key] format
    # where key == str(sect_x_y)
    # key Order == [north, northEast, east,
    #              northWest,center,southEast,
    #                west,southWest,south]
    def calcCurrentSections(self, x, y):
        currentSections = []
        mods = [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]
        c = 0
        for sect_y in range(3):
            for sect_x in range(3):
                currentSections.append(lib.dbKeyString((x + mods[c][0]),(y + mods[c][1])))
                c += 1
            
        return currentSections
    
    #Determine the offset of a section in pixels, given its assigned screen area
    def sectionScreenOffset(self,iso_px,iso_py):
        #Yes, this IS ugly code.
        #If the sections were laid out like a clock...
        px = 0
        py = 0
        if iso_px == 0:
            if iso_py == 0: #12 O'clock Section
                px = (self.WIDTH/2)
                py = 0
            if iso_py == 1: #1:30 Section
                px = (self.WIDTH/3)
                py = (self.HEIGHT/6)
            if iso_py == 2: #3 O'clock Section
                px = (self.WIDTH/6)
                py = (self.HEIGHT/3)
        if iso_px == 1:
            if iso_py == 0: #10:30 Section
                px = ((self.WIDTH/3) * 2)
                py = (self.HEIGHT/6)
            if iso_py == 1: #Center Section
                px = (self.WIDTH/2)
                py = (self.HEIGHT/3)
            if iso_py == 2: #4:30 Section
                px = (self.WIDTH/3)
                py = (self.HEIGHT/2)
        if iso_px == 2:
            if iso_py == 0:  #9 O'clock Section
                px = ((self.WIDTH/6) * 5)
                py = (self.HEIGHT/3)
            if iso_py == 1: #7:30 Section
                px = ((self.WIDTH/6) * 4)
                py = (self.HEIGHT/2)
            if iso_py == 2: #6 O'clock Section
                px = (self.WIDTH/2)
                py = ((self.HEIGHT/3) * 2)
        px -= (self.TILE_WIDTH/2) #Moves all the tiles to the left 1/2 a tile
        return (px,py)
    
