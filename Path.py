#!/usr/bin/env python
from unboundMethods import *
from AoE import *
from DjikstraMap import DjikstraMap
from Entity import Entity
from WorldView import WorldView
from World import World
#Where are you being called from?
#What do you need to know?
#What do the Djikstra Maps you will be using need to know? 

class Path:
    def __init__(self, goalKeys, entity, worldView):
        self.goalKeys   = goalKeys
        self.entity    = entity
        self.worldView = worldView
        #Create an empty DMAP & Set Goals
        self.DMAP = DjikstraMap(self.worldView.shape, self.goalKeys)
        #Set TerrainSpeed Data
        #Set impassible
        #Process map
        self.DMAP.processMap()
        #Calculate goal.

if __name__ == '__main__':
    #Exercise the path
    goalKeys = ['0_0_0']
    WORLD = World("TEST")
    entity = Entity(WORLD, '10_10_0', 'rose.png', 'Rose')
    origin = [0,0,0]
    oKey = makeKey(origin)
    shape = Cube(oKey, [21,21,1], True)
    SCREEN_SIZE = [1366, 768]
    playerView = WorldView(WORLD, oKey, shape, SCREEN_SIZE)
    p = Path(goalKeys, entity, playerView)
    print p
    for x in range(0,len(p.DMAP.coordinates)):
        for y in range(0,len(p.DMAP.coordinates[x])):
            for z in range(0,len(p.DMAP.coordinates[x][y])):
                print p.DMAP.coordinates[x][y][z].key, p.DMAP.MapVals[p.DMAP.coordinates[x][y][z].key]
    