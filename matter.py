#!/usr/bin/env python

#Matter objects are:
#-solid and have a graphical representation
#-base class for most of the other archetypes except Fields
#-give inheriting classes a method to get a tuple of their method resolution order which is equivalent to all the classes they inherit from
#
#Accepted **kwargs in self.acceptedKWARGS:
#-'imageKey' => string in form 'foo.png', which should correspond to a key
#               in one of the imageManifests
#-'name'    => either a string or None

class Matter:
    def __init__(self, **kwargs):
        self.accepted_kwargs = {'image_key': 'ISO_BASIC_64x32.png',
                                                 'name': None,
                                                 'height': 64,
                                                 'width': 32, 
                                                 'coordinate_key': None
                                               }
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key])
        ##Default name generation
        if self.name == None: #If no name given...
            try:
                #Split image_key on '.' Name == split[0]
                name = self.image_key.split('.')[0]
                self.name = name
            except:
                pass
    
    def tick(self, TICK):
        error_string = "Subclass of Matter must implement tick method"
        raise NotImplementedError(error_string)
    
    def determine_pixel_offset(self):
        error_string = "Subclass of Matter must have determine_pixel_offset method"
        raise NotImplementedError(error_string)
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
    
