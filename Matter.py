#!/usr/bin/env python

#Matter objects are:
#-solid and have a graphical representation
#-base class for most of the other archtypes except Fields
#
#Accepted **kwargs in self.acceptedKWARGS:
#-'imageKey' => string in form 'foo.png', which should correspond to a key
#               in one of the imageManifests
#-'name'    => either a string or None

class Matter:
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        
    def __init__(self, **kwargs):
        self.acceptedKWARGS = {'imageKey': 'ISO_BASIC_64x32.png', 'name': None}
        for key in self.acceptedKWARGS.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.acceptedKWARGS[key])
        ##Default name generation
        if self.name == None: #If no name given...
            try:
                #Split imageKey on '.' Name == split[0]
                name = self.imageKey.split('.')[0]
                self.name = name
            except:
                pass
    def TICK(self, TICK):
        errorString = "Subclass of Matter must implement TICK method"
        raise NotImplementedError(errorString)
    def determinePixelOffset(self):
        errorString = "Subclass of Matter must have determinePixelOffset method"
        raise NotImplementedError(errorString)