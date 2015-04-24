#!/usr/bin/env python
from Matter import Matter
from Entity import Entity
from WorldView import WorldView
#Player is a child class of Entity that:
#-Acts as a center point for a WorldView class object
#Accepted **kwargs in self.acceptedKWARGS:
#-'world' => World object that contains the entity and to whom it reports its
#            movements
#-'coordinateKey' => key string of containing Coordinate
class Player(Entity):
    def __init__(self, **kwargs):
        Matter.__init__(self, **kwargs)
        Entity.__init__(self, **kwargs)
        self.acceptedKWARGS = {
                               }
        for key in self.acceptedKWARGS.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.acceptedKWARGS[key])
        #self.playerView = WorldView(self.World, self.Shape, self.SCREEN_SIZE)