#!/usr/bin/env python

#Matter objects are:
#-solid and have a graphical representation
#-base class for most of the other archtypes
class Matter:
    def __init__(self, imageKey, name = None, tall = 0, floatOffset = [0.5,0.5]):
        self.imageKey = imageKey
        self.tall = tall
        self.name = name
        self.floatOffset = floatOffset
        self.parentCoordinate = None
    def TICK(self, TICK):
        errorString = "Subclass of Matter must implement TICK method"
        raise NotImplementedError(errorString)
    def determinePixelOffset(self):
        errorString = "Subclass of Matter must have determinePixelOffset method"
        raise NotImplementedError(errorString)