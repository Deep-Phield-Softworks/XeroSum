#!/usr/bin/env python
from unboundmethods import midpoint,  make_key,  key_to_XYZ
#This is a collection of Area of Effect template objects.
#They should take **kwarg:
#Accepted **kwargs in self.accepted_kwargs:
#-'origin' => string of Coordinate object key in form 'x_y_z'
#-'magnitude' => either an int or a int list that describes how far to extend
#                along each axis
#-'towards_neg_inf' => Boolean that determines where the origin lies in respect
#                    to the rest of the Shape's coordinates.
#                    If True, the origin is "towards negative infinity" and the
#                    rest of teh shape extends towards positive infinity along
#                    each axis.
#                    If False, the origin is in the center of the Shape, and
#                    the shape extends the value of the magnitude out from that
#                    center. (Note this means the side length is always an odd
#                    number if towards_neg_inf == False)
#And return objects with the attributes:
#-area_key_list; a list of coordinate object keys in that area.The list should be
#              in isometric render order (iterate through y, then x, then z)
#-n_dimensional_array; a multi-dimensional list with side lengths equal to the
#                    magnitude of the shapes and corresponding Coordinate key
#                    string values.

#Current issues:
#-During shape creation, there are redundant Control loops for issuing keys to
# shape.area_key_list and shape.n_dimensional_array. The control loops for both
# need to be consolidated into one loop

#Given:
#-dimensions; either a int or a list of ints
#-contains; a default value for each entry
#Return:
#-a multidimensional array with lengths equal to the magnitudes
# in the given list
def make_n_dimension(dimensions, contains = None):
    if hasattr(dimensions, '__iter__'): #If dimensions arguement has __iter__ attribute (is a list ie)...
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
    else:                                                 #If dimensions arguement is not an iterable...         
        nD = []
        nD = [nD.append(contains) for i in range(dimensions)]
    return nD

#A base class for other shapes. Usable also as a sort of null shape.
#Accepted **kwargs in self.accepted_kwargs:
#-'origin' => string of Coordinate object key in form 'x_y_z'
#-'magnitude' => either an int or a int list that describes how far to extend
#                along each axis
#-'towards_neg_inf' => Boolean that determines where the origin lies in respect
#                    to the rest of the Shape's coordinates.
#                    If True, the origin is "towards negative infinity" and the
#                    rest of teh shape extends towards positive infinity along
#                    each axis.
#                    If False, the origin is in the center of the Shape, and
#                    the shape extends the value of the magnitude out from that
#                    center. (Note this means the side length is always an odd
#                    number if towards_neg_inf == False)
class Shape:
    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __init__(self, **kwargs):
        self.accepted_kwargs = {'origin': '0_0_0',
                               'towards_neg_inf': True,
                               'magnitude': 0}
        for key in self.accepted_kwargs.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.accepted_kwargs[key]) 

#Given:

class Cube(Shape):
    def __init__(self, **kwargs):
        Shape.__init__(self, **kwargs)
        XYZ = [int(i) for i in self.origin.split('_')]#convert key to [x,y,z]
        x, y, z = XYZ[0], XYZ[1], XYZ[2] #reassign variables for code clarity

        #Create ranges for creating coordinate list
        #If magnitude is a list of dimensions...
        if hasattr(self.magnitude, '__iter__'):
            if self.towards_neg_inf == False: #origin == center...
                r = int(self.magnitude[0])
                x_range = [ x - r, x + r + 1]
                r = int(self.magnitude[1])
                y_range = [ y - r, y + r + 1]
                r = int(self.magnitude[2])
                zRange = [ z - r, z + r + 1]
                nD = [(self.magnitude[0]*2) + 1,
                      (self.magnitude[1]*2) + 1,
                      (self.magnitude[2]*2) + 1]
            else: #towards_neg_inf == True
                r = int(self.magnitude[0])
                x_range = [x, x + r]
                r = int(self.magnitude[1])
                y_range = [y, y + r]
                r = int(self.magnitude[2])
                zRange = [z, z + r]
                nD = self.magnitude
        else: #if magnitude is not a list
            if self.towards_neg_inf == False: #origin == center...
                #ranges == [origin - magnitude, origin + magnitude]
                r = int(self.magnitude)
                x_range = [ x - r, x + r]
                y_range = [ y - r, y + r]
                zRange = [ z - r, z + r]
                nD = [r*2 + 1,
                      r*2 + 1,
                      r*2 + 1]
            else: #towards_neg_inf == True
                #ranges == [origin - magnitude, origin + magnitude]
                r = int(self.magnitude)
                x_range = [ x , x + r]
                y_range = [ y , y + r]
                zRange = [ z , z + r]
                nD = [r,r,r]
        #Dimensional array with coodinate key values
        self.n_dimensional_array = make_n_dimension(nD)
        cx, cy, cz = 0, 0, 0
        for x in range(x_range[0], x_range[1]):
            for y in range(y_range[0], y_range[1]):
                cz = 0
                for z in range(zRange[0], zRange[1]):
                    #Make a key string
                    key = make_key([x,y,z])
                    self.n_dimensional_array[cx][cy][cz] = key
                    cz += 1
                cy += 1
            cx += 1
            cy = 0
        #Flat linear list of keys in render order
        self.area_key_list = []
        for y in range(y_range[0], y_range[1] + 1):
            for x in range(x_range[0], x_range[1] + 1):
                for z in range(zRange[0], zRange[1]): #Why not +1 here? dik
                    key = make_key([x,y,z]) #Make a key string
                    self.area_key_list.append(key) #Put in flat list

#Given:
#-origin as a coordinate object key in form "x_y_z"
#-magnitude to extend as either an int or a int list
#-towards_neg_inf as a boolean
#Examples: square('0_0_0', 2, True) would start at [0,0,0] and extend to [2,2,2]
#          square('0_0_0', 2, False) would have a center at [0,0,0] and
#            extend from -2 on each axis to +2 on each axis.
#Return:
#A list of coordinate object keys in  isometric render order that
#EITHER have a center of origin and extend int(magnitude) in all directions
#on (x,y) plane
#OR if towards_neg_inf == True:
#Extends from origin towards + infinity on x and y axes (origin==towards_neg_inf square)
class Square(Shape):
    def __init__(self, **kwargs):
        Shape.__init__(self, **kwargs)
        XYZ = key_to_XYZ(self.origin)
        x, y, z = XYZ[0], XYZ[1], XYZ[2]
        #Create ranges for creating coordinate list
        if hasattr(self.magnitude, '__iter__'):
            if self.towards_neg_inf == False: #origin == center...
                r = int(self.magnitude[0])
                x_range = [ x - r, x + r + 1]
                r = int(self.magnitude[1])
                y_range = [ y - r, y + r + 1]
                nD = [(self.magnitude[0] * 2) + 1, (self.magnitude[1] * 2)+1]
            else: #towards_neg_inf == True
                r = int(self.magnitude[0])
                x_range = [x, x + r]
                r = int(self.magnitude[1])
                y_range = [y, y + r]
                nD = [self.magnitude[0], self.magnitude[1]]
        else: #Else if magnitude is not a list 
            if self.towards_neg_inf == False: #origin == center...
                r = int(self.magnitude)
                x_range = [ x - r, x + r + 1]
                y_range = [ y - r, y + r + 1]
                nD = [(r * 2)+1, (r * 2)+1]
            else: #towards_neg_inf == True
                r = int(self.magnitude)
                x_range = [x, x + r]
                y_range = [y, y + r]
                nD = [r, r]
        #Flat linear list of keys in render order
        self.area_key_list = []
        self.n_dimensional_array = make_n_dimension(nD)
        for y in range(y_range[0], y_range[1]):
            for x in range(x_range[0], x_range[1]):
                key = make_key([x,y,z]) #Make a key string
                self.area_key_list.append(key) #Put in flat list  
        cx, cy = 0, 0
        for x in range(x_range[0], x_range[1]):
            for y in range(y_range[0], y_range[1]):
                key = make_key([x,y,z]) #Make a key string
                self.n_dimensional_array[cx][cy] = key
                cy += 1
            cx += 1
            cy = 0
