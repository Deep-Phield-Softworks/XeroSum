#!/usr/bin/env python

'''
Weapon is descended from Item, which is descended from Matter

Accepted **kwargs in self.accepted_kwargs:
    -'damage' => points to an 'effect' that is not yet implemented. Will probably
                 be a list or dictionary or some other data structure.
    -'weapon_range' =>  value of the range of the weapon. 1 by default
'''


class Weapon (Item) :
    def __init__(self, **kwargs):
        Item.__init__(self, **kwargs)
        self.accepted_kwargs = {'damage': 'none', 'weapon_range' : 1}
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key])


    def attack (self, target) :
        error_string = "Subclass of weapon must properly implement it's own attack method!"
        raise NotImplementedError(error_string)

    