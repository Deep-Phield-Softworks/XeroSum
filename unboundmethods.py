#!/usr/bin/env python
from time import time
from datetime import datetime
from itertools import product


TILE_WIDTH = 64
TILE_HEIGHT = 32


def midpoint(a, b):
    mid = None
    if hasattr(a, '__iter__') and hasattr(b, '__iter__'):
        if len(a) == len(b):
            mid = []
            for i in range(len(a)):
                mid.append((a[i] + b[i])/2)
    elif (not hasattr(a, '__iter__')) and (not hasattr(b, '__iter__')):
        mid = (a + b)/2
    else:
        mid = None
    return mid


def make_key(XYZ):
    key = str(XYZ[0])
    for n in XYZ[1:len(XYZ)]:
        key = key + "_" + str(n)
    return key


def key_to_XYZ(key):
    return [int(i) for i in key.split('_')]


def find_parent(coordKey):
    XYZ = key_to_XYZ(coordKey)
    parent_chunk = make_key([int(XYZ[0]/16), int(XYZ[1]/16), int(XYZ[2])])
    return parent_chunk


def within(rect, point, width=64, height=32):
    bool = False
    """(x,(y + (height/2)) ) == 9 O'clock"""
    A = rect.midleft
    """((x + (width/2)),(y + height))==6 O'clock"""
    B = rect.midbottom
    """((x + width),(y + (height/2)))==3 O'clock"""
    C = rect.midright
    """((x + (width/2)),y)==12 O'clock"""
    D = rect.midtop

    if (left_of(A, D, point) > 0):
        if (left_of(B, C, point) < 0):
            if (left_of(D, C, point) > 0):
                if (left_of(A, B, point) < 0):
                    bool = True
    return bool

"""
Given: 2 points that for a line segment and a third point
Determine if the third point is:
-"left and/or above" the line (returns a positive integer),
-"on the line" (returns 0), or
-"right and/or below" the line (returns a negative integer)
"""


def left_of(one, two, point):
    X1 = one[0]
    X2 = two[0]
    Y1 = one[1]
    Y2 = two[1]
    Px = point[0]
    Py = point[1]
    left = (X2 - X1)*(Py - Y1) - (Y2 - Y1)*(Px - X1)
    return left


def timestamp():
    return datetime.fromtimestamp(time()).strftime('%H%M%S_%Y-%m-%d')


def adjacent(a, b):
    adjacent = False
    ab = zip(a, b)
    abs_vals = [abs(p[0] - p[1]) for p in ab]
    for v in abs_vals:
        if v == 1:
            adjacent = True
        elif v > 1:
            return False
    return adjacent


def find_adjacents(key):
    dimensions = key_to_XYZ(key)
    o = [d - 1 for d in dimensions]
    d = [2 for d in dimensions]
    return [make_key(i) for i in n_dim(o,d)]


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
