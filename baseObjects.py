#!/usr/bin/env python
import pickle, os, shelve, random
from XeroInit import *
from AoE import *
from pygame import *

#World object is a controller for chunk objects. 
#Active chunks are stored in self.active. Inactive chunks are saved in the db.
#World receives the clock TICK, updates the game turn and sends the TICK to
#active chunks.
#World creating chunks according to an minimap terrain type template.
class world:
    def __init__(self, name, chunkSize = [16,16,1]):
        self.name = name
        self.chunkSize = chunkSize
        self.db = str(name) + "Shelf"
        self.active = dict()
        self.gameTurn = 0
        self.tickAccumulator = 0
    def baseTerrainChunkFill(self, chunkKey, baseArgs):
        self.activateChunk(chunkKey)
        chunk = self.active[chunkKey]
        origin = chunk.coordinatesList[0].key
        ground = square(origin, self.chunkSize, True).areaKeyList
        for c in ground:
            chunk.coordinates[c].addElement(tile(*baseArgs))
    def randomFillChunkFeature(self, chunkKey, objArgs, chance = 1, outOf = 10):
        self.activateChunk(chunkKey)
        for c in self.active[chunkKey].coordinatesList:
            r = random.randint(0,outOf - 1)
            if r < chance:
                f = feature(*objArgs)
                f.floatOffset = [random.random(),random.random()]
                f.determinePixelOffset()
                c.addElement(f)
    def activateChunk(self, key):
        if not self.active.has_key(key):
            db = shelve.open(self.db)
            if db.has_key(key): #If chunk exists..
                self.active[key] = db[key] #Load it into active chunks
            else:               #Else if chunk doesn't exist
                self.active[key] = chunk(key, self.gameTurn, self.chunkSize) #Make it and load it
                db[key] = self.active[key] #Save chunk in db
            db.close()
            self.active[key].load()
    def deactivateChunk(self, key):
        self.active[key].unload()
        db = shelve.open(self.db)
        db[key] = self.active[key]
        db.close()
    def TICK(self, TICK):
        self.tickAccumulator += TICK
        if self.tickAccumulator % 1000:
            self.gameTurn += 1
            self.tickAccumulator = self.tickAccumulator % 1000
        for chunkKey in self.active.keys():
            self.active[chunkKey].TICK(TICK, self.gameTurn)
    def addElement(self, coordinateKey, element):
        pchunk = findParent(coordinateKey)
        self.activateChunk(pchunk)
        self.active[pchunk].addElement(coordinateKey, element)

#Chunk objects are containers for organizing coordinates into sets that are
#either active or inactive. Chunks have the following properties:
#-They are bounded planes composed of ordered sets of coordinates
#-Each chunk is of uniform dimensions in x, y and z axis
#-No two chunks can contain the same coordinate object
#-Active chunks receive ticks
#-Inactive chunks store the last game turn they were active
#-The chunk that contains a given coordinate can be determined mathematically
#-The coordinates that are contain in a chunk can be determined mathematically
class chunk:
    def __init__(self, key, gameTurn, chunkSize = [16,16,1]):
        self.key = key
        self.XYZ = keyToXYZ(key)
        self.chunkSize = chunkSize
        self.gameTurnCreated = gameTurn
        self.coordinates = dict()
        self.coordinatesList = []
        self.chunkRange = self.defineChunkRange()
        self.makeCoordinates(self.chunkRange)
        self.lastActiveGameTurn = self.gameTurnCreated
    def defineChunkRange(self):
        x = self.XYZ[0] * 16
        y = self.XYZ[1] * 16
        z = self.XYZ[2] #* 16
        xRange = [ x, x + (self.chunkSize[0]-1)]
        yRange = [ y, y + (self.chunkSize[1]-1)]
        zRange = [ z, z + (self.chunkSize[2]-1)]
        return [xRange, yRange, zRange]
    def makeCoordinates(self, ranges):
        for x in range(ranges[0][0], (ranges[0][1] +1) ): 
            for y in range(ranges[1][0], (ranges[1][1] +1) ):
                for z in range(ranges[2][0], (ranges[2][1] +1) ): 
                    key = makeKey([x,y,z]) #Make a key string
                    #Make coordinate object and store it
                    c = coordinate(key) 
                    self.coordinates[key] = c
                    self.coordinatesList.append(c)
    def TICK(self, TICK, gameTurn):
        self.lastActiveGameTurn = gameTurn
        for c in self.coordinatesList:
            c.TICK(TICK)
    def addElement(self, coordinateKey, element):
        self.coordinates[coordinateKey].addElement(element)
    def load(self):
        for c in self.coordinatesList:
            c.load()
    def unload(self):
        for c in self.coordinatesList:
            c.unload()

#Coordinates objects represent a location in a x,y,z coordinate plane.
#Coordinates have the properties:
#-Low level container of the other data object types
#-The chunk that contains a given coordinate can be determined mathematically
class coordinate:
    def __init__(self, key):
        self.key = key
        self.XYZ = keyToXYZ(key)
        self.x = self.XYZ[0]
        self.y = self.XYZ[1]
        self.z = self.XYZ[2]
        self.empty = True
        self.tiles  = []
        self.features = []
        self.items    = []
        self.entities = []
        self.fields   = []
        self.parentChunk  = makeKey([self.x/16, self.y/16, self.z])
    def addElement(self, element):
        self.empty = False
        if isinstance(element, tile):
            self.tiles.append(element)
        if isinstance(element, feature):
            self.features.append(element)
        if isinstance(element, item):
            self.items.append(element)
        if isinstance(element, entity):
            self.entities.append(element)
        if isinstance(element, field):
            self.fields.append(element)
        element.parentCoordinate = self.key
    def contains(self):
        contents = []
        contents.append(self.tiles)
        contents.append(self.features)
        contents.append(self.items)
        contents.append(self.entities)
        contents.append(self.fields)
        return contents
    def TICK(self, TICK):
        if not self.empty:
            for archtype in self.contains():
                for e in archtype:
                    e.TICK(TICK)
    def load(self):
        if not self.empty:
            for e in self.entities:
                e.load()
    def unload(self):
        if not self.empty:
            for e in self.entities:
                e.unload()

#worldView is a field object to render a portion of the world.
#Given:
#-origin as a coordinate object
#-magnitude
#Return: a worldView object which:
#-world view has a shape(cube) 
#-has its own pygame surface object
#-has a render method to draw on its surface
class worldView:
    def __init__(self, world, origin, shape):
        self.world       = world
        #First determine the shape and area of view
        self.origin      = origin
        self.shape       = shape
        self.areaKeyList = self.shape.areaKeyList
        self.nD          = self.shape.nDimensionalArray
        self.prepareChunks() #Determine chunks needed and have world load them
        for x in range(len(self.nD)):
            for y in range(len(self.nD[x])) :
                for z in range(len(self.nD[x][y])):
                    cKey = self.nD[x][y][z]
                    c = self.world.active[findParent(cKey)].coordinates[cKey]
                    self.nD[x][y][z] = c
        #Next initialize render variables
        self.SCREEN_SIZE = SCREEN_SIZE
        self.surface     = pygame.Surface(SCREEN_SIZE) #Surface((width, height))
        self.hitBoxList  = []
    def prepareChunks(self):
        #Generate a list of chunks to activate
        chunks = [] #Theoretically this will be a shorter list than world.active
        #For each coordinate key in self.area
        for coordKey in self.areaKeyList:
            XYZ = keyToXYZ(coordKey)
            #determine coordinates parent chunk
            parentChunk = findParent(coordKey)
            #check if chunk key is in the list...
            if parentChunk not in chunks: #If not...
                chunks.append(parentChunk)  #Add it...
        for parentChunk in chunks:    
            self.world.activateChunk(parentChunk)
    def render(self):
        self.hitBoxList = [] #Empty hitBoxList
        halfTileWide = int(config['TILE_WIDTH']  / 2 )
        halfTileHigh = int(config['TILE_HEIGHT'] / 2 )
        xRange = range(len(self.nD))
        yRange = range(len(self.nD[0]))    
        #Render Tiles
        for y in yRange:
            for x in xRange:
                for z in range(len(self.nD[x][y])):
                    c = self.nD[x][y][z]
                    if not c.empty:
                        basepx = (x - y) * halfTileWide + PXOFFSET
                        basepy = (x + y) * halfTileHigh + PYOFFSET
                        for t in c.tiles:
                            px, py = basepx, (basepy - t.tall)
                            img = TILE_MANIFEST[t.imageKey]
                            self.surface.blit(img, (px, py))
                            rect = Rect( (px,py), (img.get_width(),img.get_height() ) )
                            self.hitBoxList.append([rect, t])
        #Render everything else
        for y in yRange:
            for x in xRange:
                for z in range(len(self.nD[x][y])):
                        c = self.nD[x][y][z]
                        if not c.empty:
                            basepx = (x - y) * halfTileWide + PXOFFSET
                            basepy = (x + y) * halfTileHigh + PYOFFSET
                            contents = c.contains()
                            for archtype in contents[1:]:
                                for element in archtype:
                                    if isinstance(element, entity):
                                        img = element.toBlit
                                    else:
                                        img = TILE_MANIFEST[element.imageKey]
                                    px = basepx + element.pixelOffsets[0]
                                    py = basepy + element.pixelOffsets[1]- element.tall - int(element.tall * element.floatOffset[1])
                                    rect = Rect( (px,py), (img.get_width(),img.get_height() ) )
                                    self.hitBoxList.append([rect, element])
                                    self.surface.blit(img, (px, py))

#Matter objects are:
#-solid and have a graphical representation
#-base class for most of the other archtypes
class matter:
    def __init__(self, imageKey, name = None, tall = 0, floatOffset = [0.5,0.5]):
        self.imageKey = imageKey
        self.tall = tall
        self.name = name
        self.floatOffset = floatOffset
        self.parentCoordinate = None
    def TICK(self, TICK):
        raise NotImplementedError("Subclass of Matter must implement TICK method")

#Tile objects are the ground.
#Tile objects are: 
#-immobile
#-cannot usually be destroyed
#-may affect travel speed through their coordinate
#-drawn first
#Examples: dirt floor, rubble floor, gravel floor
class tile(matter):
    def __init__(self, imageKey, name = None, tall = 0, speedModifier = None):
        matter.__init__(self, imageKey, name, tall)
        self.speedModifier = speedModifier
        self.floatOffset = [0.0,0.0] #Tiles should not be offset. Would create gaps
    def TICK(self, TICK):
        pass
        
#Feature objects are facets of the world that are:
#-unable to move themselves(usually)
#-cannot be picked up or carried
#-can act and be acted upon
#-may change states over time
#-destructible
#-may block travel through their coordinate
#-may block dropping items into their coordinate
#Examples would be a chest, door and a tree
class feature(matter):
    def __init__(self, imageKey, name = None, tall = 0, floatOffset = [0.5,0.5]):
        matter.__init__(self, imageKey, name, tall)
        self.floatOffset = floatOffset
        self.height = TILE_MANIFEST[self.imageKey].get_height()
        self.width  = TILE_MANIFEST[self.imageKey].get_width()
        self.pixelOffsets = self.determinePixelOffset()
    def determinePixelOffset(self):
        #px = ( self.width) - self.floatOffset[0] * self.width
        #py = (self.height) - self.floatOffset[1] * self.height
        px = ( self.width/2.0) - self.floatOffset[0] * self.width
        py = (self.height/2.0) - self.floatOffset[1] * self.height
        self.pixelOffsets = [int(px), int(py)]
    def TICK(self, TICK):
        pass    
        
#Items are objects that can be placed into inventory. They are:
#-unable to move themselves(usually)
#-movable from ground to inventory
#-may be usable
#-may be consumable
#Example: gun or loaf of bread
class item(matter):
    def __init__(self, imageKey, name = None, tall = 0, floatOffset = [0.5,0.5]):
        matter.__init__(self, imageKey, name, tall, floatOffset)
    def TICK(self, TICK):
        pass

#Entities are objects that are "alive". They can:
#-move themselves
#-be killed/destroyed
#-may pick and drop up items
#-may have an inventory
#-may use items
#-may interact with features
#-have a speed which defines how often they act
#-have an action queue that defines their actions and the time costs
#Examples: a dog, person
class entity(matter): #entity(world, coordinateKey, imageKey)
    def __init__(self, world, coordinateKey, imageKey, name = None, tall = 0, floatOffset = [0.5,0.5]):
        self.imageKey =  imageKey 
        self.spriteSheet = SPRITE_MANIFEST[self.imageKey] #spriteSheet object that provides sprite frames
        self.width   = self.spriteSheet.frameWidth
        self.height  = self.spriteSheet.frameHeight
        matter.__init__(self, imageKey, name, self.height, floatOffset)
        self.coordinateKey = coordinateKey
        self.world = world
        self.lastFrame = 0 #the rendered last frame in a "strip" of frames
        self.facing = 5
        self.lastFacing = 5
        self.animation = self.spriteSheet.animations[self.facing]
        self.frameThreshhold = 100 #167
        self.moveThreshhold  = 500
        self.tickAccumulator = 0
        self.moveAccumulator = 0
        self.path = None
        self.toBlit = self.animation[self.lastFrame]
        self.pixelOffsets = self.determinePixelOffset()
    def determinePixelOffset(self):
        px = ( TILE_WIDTH/2.0)  - (self.floatOffset[0] * self.width)
        py = ( TILE_HEIGHT/2.0) + (self.floatOffset[1] * self.height)
        return [int(px), int(py)]
    def load(self):
        self.spriteSheet = SPRITE_MANIFEST[self.imageKey]
        self.animation = self.spriteSheet.animations[self.facing]
        self.toBlit = self.animation[self.lastFrame]
    def unload(self):
        self.spriteSheet = None
        self.animation = None
        self.toBlit = None
    def TICK(self, TICK):
        pass
        #if self.path: #If path is not None
        ##Check to see if enough time has accumulated to advance frames
        #    self.tickAccumulator += TICK
        #    if self.tickAccumulator >= self.frameThreshhold:
        #        self.tickAccumulator = 0
        #        if self.lastFrame < (len(self.animation)-1):
        #            self.lastFrame += 1
        #        else:
        #            self.lastFrame = 0
        ####Putting this in to "fix" "IndexError: list index out of range"###
        #    ###This may cause other problems, but seems to stop the exception###
        #    if len(self.animation) <= self.lastFrame:
        #        self.lastFrame = len(self.animation) - 1
        #    ###Putting this in to "fix" "IndexError: list index out of range"###
        #    ###This may cause other problems, but seems to stop the exception###
        #    self.toBlit = self.animation[self.lastFrame]
        #else: #If no path use idle animation
        #    self.animation = self.spriteSheet.animations[5]
        #    self.toBlit = self.animation[self.facing]
        #def move(self, TICK, speed = 1):
        #if self.path: #If path is not None
        #    self.moveAccumulator += TICK #Add the ticks in
        #    if self.moveAccumulator >= self.moveThreshhold: #If enough ticks...
        #        self.moveAccumulator = 0 #Reset Accumulator
        #        more = self.path.advance()      #Advance the path to the next step
        #        if more:
        #            next = self.path.path[self.path.stepIndex] #Lookup next node
        #            self.facing = self.path.facings[self.path.stepIndex]
        #            self.animation = self.spriteSheet.animations[self.facing]
        #            self.section = next[0] #Set section to node's section
        #            self.MAPX = next[1] #Adjust self.MAPX
        #            self.MAPY = next[2] #Adjust self.MAPY
        #        else:
        #            self.path = None
        #            self.animation = self.spriteSheet.animations[5]
        #return [self.section, self.MAPX, self.MAPY]

#Field objects are effects or facets of the environment that:
#-can be considered to have an origin point
#-can "radiate" from their origin
#-have an area they encompass
#-can have varying magnitudes or values at different coordinates they encompass
#-may affect the coordinates they encompass
#-cannot be picked up or dropped directly
#-may be blocked by other objects
#-has a set of rules to define the shape of the area it encompasses
#-may have either a finite or infinite duration 
#Examples: a river, light from a torch, a heal spell, an attack from a gun
class field:
    def __init__(self, origin, AoEShape, magnitude, name = None):
        self.origin     = origin
        self.AoEshape   = AoEShape
        self.magnitude  = magnitude
        self.name       = name
    def TICK(self, TICK):
        pass


#Exercise the data objects    
if __name__ == '__main__':
    pass