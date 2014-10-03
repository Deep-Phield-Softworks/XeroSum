#!/usr/bin/env python
import baseObjects 

#Current issues:
#-During shape creation, there are redundant Control loops for issuing keys to
# shape.areaKeyList and shape.nDimensionalArray. The control loops for both
# need to be consolidated into one loop

#This is a collection of Area of Effect template objects.
#They should take as parameters:
#-origin as a coordinate object key in form "x_y_z"
#-magnitude as either a single int or a list of ints
#-towardsNegInf; a boolean for whether the orgign is in the center of the shape
#or if the origin is the point in the shape most towards negative infinity along
#each axes
#And return objects with the attributes:
#-areaKeyList; a list of coordinate object keys in that area.
# The list should be in isometric render order (iterate through y, then x, then z)
#-nDimensionalArray; 

#Given:
#-dimensions; either a int or a list of ints
#Return:
#-a multidimensional array with lengths equal to the magnitudes
# in the given list
def makeNDimension(dimensions):
    if hasattr(dimensions, '__iter__'):
        nD = None
        if len(dimensions) == 2:
            nD = []
            for x in range(dimensions[0]):
                nD.append([])
                for y in range(dimensions[1]):
                    nD[x].append(None)
        if len(dimensions) == 3:
            nD = []
            for x in range(dimensions[0]):
                nD.append([])
                for y in range(dimensions[1]):
                    nD[x].append([])
                    for z in range(dimensions[2]):
                        nD[x][y].append(None)
    else:
        nD = []
        nD = [nD.append(None) for i in range(dimensions)]
    return nD

#Given:
#-A pair of values or a pair of lists
#Return:
#-value of a+b/2
def midpoint(a, b):
    mid = None
    #If both are iterable...
    if hasattr(a, '__iter__') and hasattr(b, '__iter__'):
        #the length of both iterables must be equivalent
        if len(a) == len(b):
            mid = []
            for i in range(len(a)):
                mid.append((a[i] + b[i])/2)
        #'Implicit Else' mid remains None
    #Else if neither are iterable...
    elif (not hasattr(a, '__iter__')) and (not hasattr(b, '__iter__')):
        mid = (a + b)/2
    #Else they are incomparable objects
    else:
        mid = None
    return mid

#Given:
#-origin as a coordinate object key in form "x_y_z"
#-magnitude to extend as either an int or a int list
#-towardsNegInf as a boolean
class cube():
    def __init__(self, origin, magnitude, towardsNegInf = False):
        self.origin    = origin #should be coordinate object key
        self.magnitude = magnitude #int or int list that describes extent of AoE
        XYZ = baseObjects.keyToXYZ(origin)  #convert key to [x,y,z] of origin
        x, y, z = XYZ[0], XYZ[1], XYZ[2] #reassign variables for code clarity

        #Create ranges for creating coordinate list
        #If magnitude is a list of dimensions...
        if hasattr(magnitude, '__iter__'):
            if towardsNegInf == False: #origin == center...
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
            if towardsNegInf == False: #origin == center...
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
        self.nDimensionalArray = makeNDimension(nD)
        cx, cy, cz = 0, 0, 0
        for x in range(xRange[0], xRange[1]):
            for y in range(yRange[0], yRange[1]):
                cz = 0
                for z in range(zRange[0], zRange[1]):
                    key = baseObjects.makeKey([x,y,z]) #Make a key string
                    self.nDimensionalArray[cx][cy][cz] = key
                    cz += 1
                cy += 1
                
            cx += 1
            cy = 0
        #Create absolute value ranges for
        #Flat linear list of keys in render order
        self.areaKeyList = []
        for y in range(yRange[0], yRange[1] + 1):
            for x in range(xRange[0], xRange[1] + 1):
                for z in range(zRange[0], zRange[1]): #Why not +1 here? dik
                #for z in range(zRange[0], zRange[1] + 1):
                    key = baseObjects.makeKey([x,y,z]) #Make a key string
                    self.areaKeyList.append(key) #Put in flat list
                    if z >0:
                        print key 
                    
                #Dimensional array with coodinate key values
        

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
class square():
    def __init__(self, origin, magnitude, towardsNegInf = False):
        self.origin    = origin #should be coordinate object key
        self.magnitude = magnitude #int that describes extent of AoE
        XYZ = baseObjects.keyToXYZ(origin)
        x, y, z = XYZ[0], XYZ[1], XYZ[2]
        #Create ranges for creating coordinate list
        if hasattr(magnitude, '__iter__'):
            if towardsNegInf == False: #origin == center...
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
            if towardsNegInf == False: #origin == center...
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
                key = baseObjects.makeKey([x,y,z]) #Make a key string
                self.areaKeyList.append(key) #Put in flat list
                
        cx, cy = 0, 0
        #print "len(self.areaKeyList)", len(self.areaKeyList)
        for x in range(xRange[0], xRange[1]):
            for y in range(yRange[0], yRange[1]):
                key = baseObjects.makeKey([x,y,z]) #Make a key string
                #print "key", key, "cx", cx, "cy", cy
                self.nDimensionalArray[cx][cy] = key
                cy += 1
            cx += 1
            cy = 0
if __name__ == '__main__':
    pass
    