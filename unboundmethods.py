#!/usr/bin/env python
from time import time
from datetime import datetime


TILE_WIDTH = 64
TILE_HEIGHT = 32
#Given:
#-A pair of values or a pair of lists
#Return:
#-value of a+b/2 or None if incomparable objects
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

#Given:  List of ints
#Return: String for use as a dictionary key in form: "x_y_z"
def make_key(XYZ):
    key = str(XYZ[0])
    for n in XYZ[1:len(XYZ)]:
        key = key + "_" + str(n)
    return key

#Given:  String in form: "int_int_int"
#Return: List of ints
def key_to_XYZ(key):
    #print "KEY:",  key
    XYZ = [int(i) for i in key.split('_')]
    return XYZ

#Given: String in form: "int_int_int"
#Return: Parent chunk key string in form: "intX_intY_intZ"
def find_parent(coordKey):
    XYZ = key_to_XYZ(coordKey)
    parent_chunk = make_key([int(XYZ[0]/16),
                           int(XYZ[1]/16),
                           int(XYZ[2])] )
    return parent_chunk

#Given: (x,y) of a mouse click
#Determine if the click is within a tile shaped diamond
def within(rect, point, width = 64, height = 32):
    bool = False
    #4 points that define the rhombus
    A = rect.midleft#(x,(y + (height/2)) )           #9 O'clock
    B = rect.midbottom#((x + (width/2)),(y + height))  #6 O'clock
    C = rect.midright#((x + width),(y + (height/2))) #3 O'clock
    D = rect.midtop#((x + (width/2)),y)             #12 O'clock 

    if (left_of(A,D,point) > 0):
        if (left_of(B,C,point) < 0):
            if (left_of(D,C,point) > 0):
                if (left_of(A,B,point) < 0):
                    bool = True
    return bool

#Given: 2 points that for a line segment and a third point
#Determine if the third point is:
#-"left and/or above" the line (returns a positive integer),
#-"on the line" (returns 0), or
#-"right and/or below" the line (returns a negative integer)
def left_of(one, two, point):
    X1 = one[0]
    X2 = two[0]
    Y1 = one[1]
    Y2 = two[1]
    Px = point[0]
    Py = point[1]
    left = (X2 - X1)*(Py - Y1) - (Y2 - Y1)*(Px - X1)
    return left
    
#Given: Nothing
#Return a timestamp string
def timestamp():
    return datetime.fromtimestamp(time()).strftime('%H%M%S_%Y-%m-%d')
