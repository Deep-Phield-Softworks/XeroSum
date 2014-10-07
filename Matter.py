#!/usr/bin/env python

#Matter objects are:
#-solid and have a graphical representation
#-base class for most of the other archtypes
class Matter:
    def __init__(self, imageKey, name = None):
        self.imageKey = imageKey
        #Default name generation
        if name == None: #If no name given...
            name = imageKey.split('.')[0]#Split imageKey on '.' Name == split[0]
        self.name = name
    def TICK(self, TICK):
        errorString = "Subclass of Matter must implement TICK method"
        raise NotImplementedError(errorString)
    def determinePixelOffset(self):
        errorString = "Subclass of Matter must have determinePixelOffset method"
        raise NotImplementedError(errorString)