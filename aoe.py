#!/usr/bin/env python
from unboundmethods import midpoint,  make_key,  key_to_XYZ
from unboundmethods import axis, n_dim, shaped_3d_array

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
        self.n_dim = n_dim(self.origin, self.magnitude)
        sorted_tuples = sorted(self.n_dim, key=itemgetter(1, 0, 2))
        self.render_key_list = [make_key(t) for t in sorted_tuples]
        self.shaped_3d_array = shaped_3d_array(self.origin, self.magnitude)
