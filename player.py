#!/usr/bin/env python
from matter import Matter
from entity import Entity
from worldview import WorldView

#Player is a child class of Entity that:
#-Acts as a center point for a WorldView class object
#Accepted **kwargs in self.acceptedKWARGS:
#-'world' => World object that contains the entity and to whom it reports its
#            movements
#-'coordinateKey' => key string of containing Coordinate
class Player(Entity):
    def __init__(self, **kwargs):
        Entity.__init__(self, **kwargs)
        self.accepted_kwargs = {
                               }
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key])
        #self.player_view = WorldView(self.world, self.shape, self.SCREEN_SIZE)
