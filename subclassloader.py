#!/usr/bin/env python
import os
import sys


from tile import Tile
from feature import Feature
from item import Item
from entity import Entity
from field import Field


"""
#SubclassLoader is meant to offer a flexible way to automatically import many
#subclass modules for classes that need to be aware of them. Expected classes
#that may need to be aware of all the archtype subclasses are: Coordinate,
#Entity and possibly World.
"""

os.chdir(sys.path[0])
sys.path.append(str(sys.path[0]) + os.sep + 'subclasses')

libnames = []
filenames = os.listdir('subclasses')
for name in filenames:
    s = str(name).split(".")
    if s[1] == 'py':
        libnames.append(s[0])

for libname in libnames:
    try:
        lib = __import__(libname)
    except:
        print sys.exc_info()
    else:
        globals()[libname] = lib
if __name__ == '__main__':
    print testCase.test
