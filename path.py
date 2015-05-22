#!/usr/bin/env python
from unboundmethods import *
from aoe import *
from dmap import DijkstraMap
from entity import Entity
from world import World
#Path objects keep track of the path of an entity
#Given:
#-goalKeys, a list of coordinate object keys
#-entity, the Entity object to whom the path belongs
#-shape, the shape object that contains info on coordinates involved
#Produce a Path object which has:
#-self.nodes, list of coordinate keys from self.entity.parentCoordinate to
# one of the goalKeys
#-self.step_index, an int of the index of the current step along self.nodes
#-self.facings, a list of int headings that correspond to SpriteSheet strip
# indexes and set the apparent heading for each step index
class Path:
    def __init__(self, goal_dict, entity, shape):
        self.goal_dict   = goal_dict
        self.entity    = entity
        self.shape     = shape
        #Create an empty DMAP & Set Goals
        self.DMAP = DijkstraMap(shape, self.goal_dict)
        #Make DMAP with Terrain Speed modifier Data and impassible data
        self.speed_map = self.make_speed_map()
        #Combine DMAPS
        self.DMAP.combine(self.speed_map)
        #Process map
        self.DMAP.process_map()
        #Generate list of nodes' keys
        self.nodes = self.DMAP.find_path(self.entity.coordinate_key)
        self.step_index = 0
        #Create facing list
        self.create_facings()
    
    #Create DMAP populated with Terrain speeds and impassible terrain
    def make_speed_map(self):
        selected_dict = dict()
        for key in self.shape.area_key_list:
            val = 10000
            c = self.entity.world.get_coordinate_obj(key)
            for archetype in c.contains():
                for element in archetype:
                    if val:
                        if hasattr(element, 'speedModifier'):
                            val = int(val * element.speedModifier)
                        if hasattr(element, 'impassible'):
                            if element.impassible:
                                val = None
            selected_dict[key] = val
        return DijkstraMap(self.shape, selected_dict)
    
    #Move the path step index forward one node
    #Return None if no more path or the next node key
    def advance(self):
        next = None
        if not self.step_index + 1 >= len(self.nodes):
            self.step_index += 1
            next = self.nodes[self.step_index]
        return next    
    
    def create_facings(self):
        self.facings = []
        #If there is more than one node in path...
        if (len(self.nodes)) > 1:
            start = self.nodes[0] #set start node
            #foreach node in range...
            for node in range(1,len(self.nodes)):
                XYZ1 = key_to_XYZ(start)
                XYZ2 = key_to_XYZ(self.nodes[node])
                #compare the x and y values
                x1 = XYZ1[0]
                y1 = XYZ1[1]
                x2 = XYZ2[0]
                y2 = XYZ2[1]
                #Must use isometric headings here
                if x1 == x2:
                    if y2 < y1: #Heading NE
                        face = 9
                    else: #if y2 > y1 Heading SW
                        face = 1
                elif x1 < x2:
                    if y2 < y1: #Heading Due E
                        face = 6
                    elif y2 == y1: #Heading SE
                        face = 3
                    else: #Heading Due S
                        face = 2
                else: #if x1 > x2
                    if y2 < y1: #Heading Due N
                        face = 8
                    elif y2 == y1: #Heading NW
                        face = 7 
                    else: #Heading Due W
                        face = 4  
                self.facings.append(face)    
                start = self.nodes[node]
        else:
            self.facings.append(self.entity.facing)
        self.facings.append(self.facings[-1])
