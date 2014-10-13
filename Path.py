#!/usr/bin/env python
from unboundMethods import *
from AoE import *
from DijkstraMap import DijkstraMap
from Entity import Entity
from WorldView import WorldView
from World import World
#Path objects keep track of the path of an entity
#Given:
#-goalKeys, a list of coordinate object keys
#-entity, the Entity object to whom the path belongs
#-shape, the shape object that contains info on coordinates involved
#Produce a Path object which has:
#-self.nodes, list of coordinate keys from self.entity.parentCoordinate to
# one of the goalKeys
#-self.stepIndex, an int of the index of the current step along self.nodes
#-self.facings, a list of int headings that correspond to SpriteSheet strip
# indexes and set the apparent heading for each step index
class Path:
    def __init__(self, goalDict, entity, shape):
        self.goalDict   = goalDict
        self.entity    = entity
        self.shape     = shape
        #Create an empty DMAP & Set Goals
        self.DMAP = DijkstraMap(shape, self.goalDict)
        #Make DMAP with Terrain Speed modifier Data and impassible data
        self.speedMap = self.makeSpeedMap()
        #Combine DMAPS
        self.DMAP.combine(self.speedMap)
        #Process map
        self.DMAP.processMap()
        #Generate list of nodes' keys
        self.nodes = self.DMAP.findPath(self.entity.coordinateKey)
        self.stepIndex = 0
        #Create facing list
        self.createFacings()   
    
    #Create DMAP populated with Terrain speeds and impassible terrain
    def makeSpeedMap(self):
        selectedDict = dict()
        for key in self.shape.areaKeyList:
            val = 10000
            c = self.entity.world.getCoordinateObj(key)
            for archtype in c.contains():
                for element in archtype:
                    if hasattr(element, 'speedModifier'):
                        val = int(val * element.speedModifier)
                    if hasattr(element, 'impassible'):
                        if element.impassible:
                            val = None
            selectedDict[key] = val
        return DijkstraMap(self.shape, selectedDict)
    
    #Move the path step index forward one node
    #Return a boolean of whether there was another step
    def advance(self):
        more = True
        if self.stepIndex + 1 >= len(self.nodes):
            more = False
        else:
            self.stepIndex += 1
        return more    
    
    def createFacings(self):
        self.facings = []
        #If there is more than one node in path...
        if (len(self.nodes)) > 1:
            start = self.nodes[0] #set start node
            #foreach node in range...
            for node in range(1,len(self.nodes)):
                XYZ1 = keyToXYZ(start)
                XYZ2 = keyToXYZ(self.nodes[node])
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
   
if __name__ == '__main__':
    #Exercise the path
    
    WORLD = World("TEST")
    entity = Entity(WORLD, '10_10_0', 'rose.png', 'Rose')
    origin = [0,0,0]
    oKey = makeKey(origin)
    goalDict = dict()
    goalDict[oKey] = 0
    shape = Cube(oKey, [21,21,1], True)
    SCREEN_SIZE = [1366, 768]
    playerView = WorldView(WORLD, shape, SCREEN_SIZE)
    p = Path(goalDict, entity, playerView.shape)
    print p.nodes
    print p.facings
    
    #for x in range(0,len(p.DMAP.coordinates)):
    #    for y in range(0,len(p.DMAP.coordinates[x])):
    #        for z in range(0,len(p.DMAP.coordinates[x][y])):
    #            print p.DMAP.coordinates[x][y][z].key, p.DMAP.MapVals[p.DMAP.coordinates[x][y][z].key]
    #