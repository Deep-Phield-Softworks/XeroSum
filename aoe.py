#!/usr/bin/env python
from itertools import product
from operator import itemgetter
import pprint


from BTrees.OOBTree import OOBTree
from persistent.mapping import PersistentMapping as pdict
from persistent.list import PersistentList as plist


from unboundmethods import midpoint,  make_key,  key_to_XYZ

'''
This is a collection of Area of Effect template objects.
They should take **kwarg:
Accepted **kwargs in self.accepted_kwargs:
-'origin' => string of Coordinate object key in form 'x_y_z'
-'magnitude' =>  int list that describes how far to extend
                            along each axis; values can be positive or negative
And return objects with the attributes:
-render_key_list; a list of coordinate object keys in that area.The list should
            be in isometric render order (iterate through y, then x, then z)
-shaped_3d_array; a multi-dimensional list with Coordinate key
                string values.

A base class for other shapes. Usable also as a sort of null shape.
Accepted **kwargs in self.accepted_kwargs:
-'origin' => string of Coordinate object key in form 'x_y_z'
-'magnitude' => int list that describes how far to extend
                along each axis and in what direction with sign
'''


class Shape:

    def __init__(self, **kwargs):
        self.accepted_kwargs = {
                                'origin': [0, 0, 0],
                                'magnitude': [1, 1, 1]
                                                }
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key])

    def __setattr__(self, name, value):
            self.__dict__[name] = value


class Cuboid(Shape):

    def __init__(self, **kwargs):
        Shape.__init__(self, **kwargs)
        self.n_dim = plist(n_dim(self.origin, self.magnitude))
        sorted_tuples = sorted(self.n_dim, key=itemgetter(1, 0, 2))
        self.render_key_list = plist([make_key(t) for t in sorted_tuples])
        self.shaped_3d_array = shaped_3d_array(self.origin, self.magnitude)


def n_dim(origin=[0, 0, 0], dimensions=[1, 1, 1]):
    return list(product(*[axis(*pair) for pair in zip(origin, dimensions)]))


def shaped_3d_array(origin=[0, 0, 0], dimensions=[1, 1, 1]):
    n = [axis(*z) for z in zip(origin, dimensions)]
    s = [[[make_key((x, y, z)) for z in n[2]] for y in n[1]] for x in n[0]]
    return s


def axis(start, stop):
    i = 1
    if start > stop:
        i = -1
    return list(xrange(start, stop, i))
