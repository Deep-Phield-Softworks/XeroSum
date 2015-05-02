#!/usr/bin/env python
from pygame import Rect, Surface
from operator import *
from unboundmethods import find_parent, TILE_WIDTH, TILE_HEIGHT
from imagemanifests import *
from subclassloader import *
#from Tile import Tile
#from Feature import Feature
#from Item import Item
#from Entity import Entity
#from Field import Field
#worldView is an object made to render a portion of the world.
#Given:
#-world object
#-shape object
#-screen_size as tuple in form (SCREEN_WIDTH, SCREEN_HEIGHT)
#Return: a worldView object which:
#-world view has a shape(cube) 
#-has its own pygame surface object
#-has a render method to draw on its surface
#-activates needed chunks from the world given
#-Stores a list of hit boxes for objects rendered in list with elements in
# form: [pygame.Rect, Object]
class WorldView:
    def __init__(self, world, shape, screen_size):
        self.world       = world 
        self.shape       = shape 
        self.area_key_list = self.shape.area_key_list
        self.nD          = self.shape.n_dimensional_array
        self.prepare_chunks() #Determine chunks needed and have world load them
        self.preload_coordinates() #Overwrite self.nD with coordinates objects
        self.screen_size = screen_size
        self.surface     = Surface(screen_size) #Surface((width, height))
        self.hit_box_list  = []
    def prepare_chunks(self):
        #Generate a list of chunks to activate
        chunks = []
        #For each coordinate key in self.area
        for coord_key in self.area_key_list:
            #determine coordinates parent chunk
            parent_chunk = find_parent(coord_key)
            #check if chunk key is in the list...
            if parent_chunk not in chunks: #If not...
                chunks.append(parent_chunk)  #Add it...
        self.world.activate_chunk(*chunks)
    def preload_coordinates(self):
        half_tile_wide = int(TILE_WIDTH  / 2 ) #imported from unboundMethods
        half_tile_high = int(TILE_HEIGHT / 2 ) #imported from unboundMethods
        for x in range(len(self.nD)):
            for y in range(len(self.nD[x])) :
                for z in range(len(self.nD[x][y])):
                    cKey = self.nD[x][y][z]
                    c = self.world.db['active_chunks'][find_parent(cKey)].coordinates[cKey]
                    basepx = (x - y) * half_tile_wide + px_offset
                    basepy = (x + y) * half_tile_high + py_offset
                    self.nD[x][y][z] = c, (basepx, basepy)
    def render(self):
        self.surface.fill((0,0,0)) #Fill surface to avoid map edge slug trails 
        self.hit_box_list = [] #Empty hit_box_list
        unsorted = []
        x_range = range(len(self.nD))
        y_range = range(len(self.nD[0]))    
        #Render Tiles
        for y in y_range:
            for x in x_range:
                for z in range(len(self.nD[x][y])):
                    c   = self.nD[x][y][z][0] #c is now the Coordinate object
                    px = self.nD[x][y][z][1][0] 
                    py = self.nD[x][y][z][1][1]
                    contents = c.list_all()    #get all contents
                    for e in contents:
                        #Determine proper image
                        if isinstance(e, Entity):
                            e.determine_pixel_offset() #Update offset info
                            img = e.to_blit()
                        else:
                            img = tile_manifest[e.image_key]
                        #Adjust px,py based upon e's attributes
                        px = px + e.pixel_offsets[0]
                        py = py + e.pixel_offsets[1]
                        #Create hit box rect and add to hit_box_list
                        rect = Rect( (px,py), (img.get_width(),img.get_height() ) )
                        self.hit_box_list.append([rect, e])
                        unsorted.append([img, e.layer, py, px, e])
        #Sort render elements by layer, py, px
        render_list = sorted(unsorted, key= itemgetter(1,2,3))
        for e in render_list:
            self.surface.blit(e[0], (e[3], e[2]))