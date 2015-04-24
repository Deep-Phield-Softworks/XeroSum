#!/usr/bin/env python
#SubclassLoader is meant to offer a flexible way to automatically import many
#subclass modules for classes that need to be aware of them. Expected classes
#that may need to be aware of all the archtype subclasses are: Coordinate,
#Entity and possibly World.
import os, sys
from Tile import Tile
from Feature import Feature
from Item import Item
from Entity import Entity
from Field import Field
#Change the CWD to wherever this script resides
os.chdir(sys.path[0])
sys.path.append(str(sys.path[0])+ os.sep + 'subclasses')
#Create the list of modules to load
libnames = []
unsplit = os.listdir('subclasses') #Pull a list of files in 'subclasses' folder
for name in unsplit:
    s = str(name).split(".") #Split filenames on the '.'
    if s[1] == 'py':         #If second half of the filename split is 'py'...
        libnames.append(s[0])#Then include it in the list. 
#This code snippet is from Stack Overflow. Thank you Stack Overflow!
for libname in libnames:
    try:
        lib = __import__(libname)
    except:
        print sys.exc_info()
    else:
        globals()[libname] = lib
if __name__ == '__main__':
    print testCase.test    