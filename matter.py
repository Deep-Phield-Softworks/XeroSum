#!/usr/bin/env python
from persistent.list import PersistentList as plist


'''
Matter objects are:
-solid and have a graphical representation
-base class for most of the other archetypes except Fields
-give inheriting classes a method to get a tuple of their
method resolution order which is equivalent to all the classes
they inherit from

Accepted **kwargs in self.acceptedKWARGS:
-'imageKey' => string in form 'foo.png', which should correspond
            to a key in one of the image Manifests
-'name' => either a string or None
-'width' => width in pixels
-'height' => length in pixels
-'coordinate_key' => string key of coordinate object that contains matter
-'parent_coordinate' => reference to coordinate object that contains matter
-'effects' => persistent list for containing Effects affecting the Matter
'''


class Matter:
    def __init__(self, **kwargs):
        self.accepted_kwargs = {'image_key': 'ISO_BASIC_64x32.png',
                                'name': None,
                                'width': 32,
                                'height': 64,
                                'coordinate_key': None,
                                'parent_coordinate': None,
                                'effects': plist([])
                                }
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key])
        # Default name generation
        if self.name is None:  # If no name given...
            try:
                # Split image_key on '.' Name == split[0]
                name = self.image_key.split('.')[0]
                self.name = name
            except:
                pass

    def tick(self, TICK):
        error_string = "Subclass of Matter must implement tick method"
        raise NotImplementedError(error_string)

    def process_effects(self):
        error_string = "Subclass of Matter needs process_effects method"
        raise NotImplementedError(error_string)

    def deactivate(self):
        error_string = "Subclass of Matter needs deactivate method"
        raise NotImplementedError(error_string)

    def determine_pixel_offset(self):
        error_string = "Subclass of Matter needs determine_pixel_offset method"
        raise NotImplementedError(error_string)

    def to_blit(self):
        error_string = "Subclass of Matter must have to_blit method"
        raise NotImplementedError(error_string)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
