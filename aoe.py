#!/usr/bin/env python
from unboundmethods import midpoint,  make_key,  key_to_XYZ
#This is a collection of Area of Effect template objects.
#They should take **kwarg:
#Accepted **kwargs in self.acceptedKWARGS:
#-'origin' => string of Coordinate object key in form 'x_y_z'
#-'magnitude' => either an int or a int list that describes how far to extend
#                along each axis
#-'towardsNegInf' => Boolean that determines where the origin lies in respect
#                    to the rest of the Shape's coordinates.
#                    If True, the origin is "towards negative infinity" and the
#                    rest of teh shape extends towards positive infinity along
#                    each axis.
#                    If False, the origin is in the center of the Shape, and
#                    the shape extends the value of the magnitude out from that
#                    center. (Note this means the side length is always an odd
#                    number if towardsNegInf == False)
#And return objects with the attributes:
#-areaKeyList; a list of coordinate object keys in that area.The list should be
#              in isometric render order (iterate through y, then x, then z)
#-nDimensionalArray; a multi-dimensional list with side lengths equal to the
#                    magnitude of the shapes and corresponding Coordinate key
#                    string values.

#Current issues:
#-During shape creation, there are redundant Control loops for issuing keys to
# shape.areaKeyList and shape.nDimensionalArray. The control loops for both
# need to be consolidated into one loop

#Given:
#-dimensions; either a int or a list of ints
#-contains; a default value for each entry
#Return:
#-a multidimensional array with lengths equal to the magnitudes
# in the given list
def makeNDimension(dimensions, contains = None):
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
    else:
        nD = []
        nD = [nD.append(None) for i in range(dimensions)]
    return nD

#A base class for other shapes. Usable also as a sort of null shape.
#Accepted **kwargs in self.acceptedKWARGS:
#-'origin' => string of Coordinate object key in form 'x_y_z'
#-'magnitude' => either an int or a int list that describes how far to extend
#                along each axis
#-'towardsNegInf' => Boolean that determines where the origin lies in respect
#                    to the rest of the Shape's coordinates.
#                    If True, the origin is "towards negative infinity" and the
#                    rest of teh shape extends towards positive infinity along
#                    each axis.
#                    If False, the origin is in the center of the Shape, and
#                    the shape extends the value of the magnitude out from that
#                    center. (Note this means the side length is always an odd
#                    number if towardsNegInf == False)
class Shape:
    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __init__(self, **kwargs):
        self.acceptedKWARGS = {'origin': '0_0_0',
                               'towardsNegInf': True,
                               'magnitude': 0}
        for key in self.acceptedKWARGS.keys():
            if key in kwargs.keys():
                self.__setattr__(key, kwargs[key])
            else:
                self.__setattr__(key, self.acceptedKWARGS[key]) 

#Given:

class Cube(Shape):
    def __init__(self, **kwargs):
        Shape.__init__(self, **kwargs)
        XYZ = [int(i) for i in self.origin.split('_')]#convert key to [x,y,z]
        x, y, z = XYZ[0], XYZ[1], XYZ[2] #reassign variables for code clarity

        #Create ranges for creating coordinate list
        #If magnitude is a list of dimensions...
        if hasattr(self.magnitude, '__iter__'):
            if self.towardsNegInf == False: #origin == center...
                r = int(self.magnitude[0])
                xRange = [ x - r, x + r + 1]
                r = int(self.magnitude[1])
                yRange = [ y - r, y + r + 1]
                r = int(self.magnitude[2])
                zRange = [ z - r, z + r + 1]
                nD = [(self.magnitude[0]*2) + 1,
                      (self.magnitude[1]*2) + 1,
                      (self.magnitude[2]*2) + 1]
            else: #towardsNegInf == True
                r = int(self.magnitude[0])
                xRange = [x, x + r]
                r = int(self.magnitude[1])
                yRange = [y, y + r]
                r = int(self.magnitude[2])
                zRange = [z, z + r]
                nD = self.magnitude
        else: #if magnitude is not a list
            if self.towardsNegInf == False: #origin == center...
                #ranges == [origin - magnitude, origin + magnitude]
                r = int(self.magnitude)
                xRange = [ x - r, x + r]
                yRange = [ y - r, y + r]
                zRange = [ z - r, z + r]
                nD = [r*2 + 1,
                      r*2 + 1,
                      r*2 + 1]
            else: #towardsNegInf == True
                #ranges == [origin - magnitude, origin + magnitude]
                r = int(self.magnitude)
                xRange = [ x , x + r]
                yRange = [ y , y + r]
                zRange = [ z , z + r]
                nD = [r,r,r]
        #Dimensional array with coodinate key values
        self.nDimensionalArray = makeNDimension(nD)
        cx, cy, cz = 0, 0, 0
        for x in range(xRange[0], xRange[1]):
            for y in range(yRange[0], yRange[1]):
                cz = 0
                for z in range(zRange[0], zRange[1]):
                    #Make a key string
                    key = make_key([x,y,z])
                    self.nDimensionalArray[cx][cy][cz] = key
                    cz += 1
                cy += 1
            cx += 1
            cy = 0
        #Flat linear list of keys in render order
        self.areaKeyList = []
        for y in range(yRange[0], yRange[1] + 1):
            for x in range(xRange[0], xRange[1] + 1):
                for z in range(zRange[0], zRange[1]): #Why not +1 here? dik
                    key = make_key([x,y,z]) #Make a key string
                    self.areaKeyList.append(key) #Put in flat list

#Given:
#-origin as a coordinate object key in form "x_y_z"
#-magnitude to extend as either an int or a int list
#-towardsNegInf as a boolean
#Examples: square('0_0_0', 2, True) would start at [0,0,0] and extend to [2,2,2]
#          square('0_0_0', 2, False) would have a center at [0,0,0] and
#            extend from -2 on each axis to +2 on each axis.
#Return:
#A list of coordinate object keys in  isometric render order that
#EITHER have a center of origin and extend int(magnitude) in all directions
#on (x,y) plane
#OR if towardsNegInf == True:
#Extends from origin towards + infinity on x and y axes (origin==towardsNegInf square)
class Square(Shape):
    def __init__(self, **kwargs):
        Shape.__init__(self, **kwargs)
        XYZ = key_to_XYZ(self.origin)
        x, y, z = XYZ[0], XYZ[1], XYZ[2]
        #Create ranges for creating coordinate list
        if hasattr(self.magnitude, '__iter__'):
            if self.towardsNegInf == False: #origin == center...
                r = int(self.magnitude[0])
                xRange = [ x - r, x + r + 1]
                r = int(self.magnitude[1])
                yRange = [ y - r, y + r + 1]
                nD = [(self.magnitude[0] * 2) + 1, (self.magnitude[1] * 2)+1]
            else: #towardsNegInf == True
                r = int(self.magnitude[0])
                xRange = [x, x + r]
                r = int(self.magnitude[1])
                yRange = [y, y + r]
                nD = [self.magnitude[0], self.magnitude[1]]
        else: #Else if magnitude is not a list 
            if self.towardsNegInf == False: #origin == center...
                r = int(self.magnitude)
                xRange = [ x - r, x + r + 1]
                yRange = [ y - r, y + r + 1]
                nD = [(r * 2)+1, (r * 2)+1]
            else: #towardsNegInf == True
                r = int(self.magnitude)
                xRange = [x, x + r]
                yRange = [y, y + r]
                nD = [r, r]
        #Flat linear list of keys in render order
        self.areaKeyList = []
        self.nDimensionalArray = makeNDimension(nD)
        for y in range(yRange[0], yRange[1]):
            for x in range(xRange[0], xRange[1]):
                key = make_key([x,y,z]) #Make a key string
                self.areaKeyList.append(key) #Put in flat list  
        cx, cy = 0, 0
        for x in range(xRange[0], xRange[1]):
            for y in range(yRange[0], yRange[1]):
                key = make_key([x,y,z]) #Make a key string
                self.nDimensionalArray[cx][cy] = key
                cy += 1
            cx += 1
            cy = 0
