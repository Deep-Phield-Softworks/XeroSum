#!/usr/bin/env python
from itertools import product

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
-area_key_list; a list of coordinate object keys in that area.The list should
            be in isometric render order (iterate through y, then x, then z)
-n_dimensional_array; a multi-dimensional list with Coordinate key
                string values.
'''


def n_dim(origin=[0, 0, 0], dimensions=[1, 1, 1]):
    return list(product(*[axis(*pair) for pair in zip(origin, dimensions)]))


def axis(start, stop):
    i = 1
    if start > stop:
        i = -1
    return range(start, stop, i)


def make_n_dimension(dimensions, contains=None):
    # If dimensions arguement has __iter__ attribute (is a list ie)...
    if hasattr(dimensions, '__iter__'):
        nD = None
        if len(dimensions) == 2:
            nD = []
            for x in range(dimensions[0]):
                nD.append([])
                for y in range(dimensions[1]):
                    nD[x].append(contains)
        if len(dimensions) == 3:
            nD = []
            for x in range(dimensions[0]):
                nD.append([])
                for y in range(dimensions[1]):
                    nD[x].append([])
                    for z in range(dimensions[2]):
                        nD[x][y].append(contains)
    else:  # If dimensions arguement is not an iterable...
        nD = []
        nD = [nD.append(contains) for i in range(dimensions)]
    return nD


'''
A base class for other shapes. Usable also as a sort of null shape.
Accepted **kwargs in self.accepted_kwargs:
-'origin' => string of Coordinate object key in form 'x_y_z'
-'magnitude' => either an int or a int list that describes how far to extend
                along each axis
-'towards_neg_inf' => Boolean that determines where the origin lies in respect
                    to the rest of the Shape's coordinates.
                    If True, the origin is "towards negative infinity" and the
                    rest of teh shape extends towards positive infinity along
                    each axis.
                    If False, the origin is in the center of the Shape, and
                    the shape extends the value of the magnitude out from that
                    center. (Note this means the side length is always an odd
                    number if towards_neg_inf == False)
'''


class Shape:

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __init__(self, **kwargs):
        self.accepted_kwargs = {'origin': '0_0_0',
                                'magnitude': [1, 1, 1]}
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key])


class Cube(Shape):

    def __init__(self, **kwargs):
        Shape.__init__(self, **kwargs)
        # convert key to [x,y,z]
        XYZ = [int(i) for i in self.origin.split('_')]
        # reassign variables for code clarity
        x, y, z = XYZ[0], XYZ[1], XYZ[2]

        # Create ranges for creating coordinate list
        # If magnitude is a list of dimensions...
        if hasattr(self.magnitude, '__iter__'):
            # PEP8 suggests changing this to 'is False' ???
            if not self.towards_neg_inf:  # origin == center...
                r = int(self.magnitude[0])
                x_range = [x - r, x + r + 1]
                r = int(self.magnitude[1])
                y_range = [y - r, y + r + 1]
                r = int(self.magnitude[2])
                zRange = [z - r, z + r + 1]
                nD = [(self.magnitude[0]*2) + 1,
                      (self.magnitude[1]*2) + 1,
                      (self.magnitude[2]*2) + 1]
            else:  # towards_neg_inf == True
                r = int(self.magnitude[0])
                x_range = [x, x + r]
                r = int(self.magnitude[1])
                y_range = [y, y + r]
                r = int(self.magnitude[2])
                zRange = [z, z + r]
                nD = self.magnitude
        else:  # if magnitude is not a list
            # PEP 8 suggests changing to 'is False' ???
            if not self.towards_neg_inf:  # origin == center...
                # ranges == [origin - magnitude, origin + magnitude]
                r = int(self.magnitude)
                x_range = [x - r, x + r]
                y_range = [y - r, y + r]
                zRange = [z - r, z + r]
                nD = [r*2 + 1,
                      r*2 + 1,
                      r*2 + 1]
            else:  # towards_neg_inf == True
                # ranges == [origin - magnitude, origin + magnitude]
                r = int(self.magnitude)
                x_range = [x, x + r]
                y_range = [y, y + r]
                zRange = [z, z + r]
                nD = [r, r, r]
        # Dimensional array with coodinate key values
        self.n_dimensional_array = make_n_dimension(nD)
        cx, cy, cz = 0, 0, 0
        for x in range(x_range[0], x_range[1]):
            for y in range(y_range[0], y_range[1]):
                cz = 0
                for z in range(zRange[0], zRange[1]):
                    # Make a key string
                    key = make_key([x, y, z])
                    self.n_dimensional_array[cx][cy][cz] = key
                    cz += 1
                cy += 1
            cx += 1
            cy = 0
        # Flat linear list of keys in render order
        self.area_key_list = []
        for y in range(y_range[0], y_range[1] + 1):
            for x in range(x_range[0], x_range[1] + 1):
                for z in range(zRange[0], zRange[1]):  # Why not +1 here? dik
                    key = make_key([x, y, z])  # Make a key string
                    self.area_key_list.append(key)  # Put in flat list

if __name__ == "__main__":
    o = [0, 0, 0]
    d = [3, -3, 3]
    l = n_dim(o, d)
    for i in l:
        print i
