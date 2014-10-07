#!/usr/bin/env python
import os, sys
#Change the CWD to wherever this script resides
os.chdir(sys.path[0])
sys.path.append(str(sys.path[0])+ os.sep + 'subclasses')
print sys.path[0]
libnames = []
unsplit = os.listdir('subclasses')
for name in unsplit:
    s = str(name).split(".")
    libnames.append(s[0])
for libname in libnames:
    try:
        lib = __import__(libname)
    except:
        print sys.exc_info()
    else:
        globals()[libname] = lib
print testCase.test
#if __name__ == '__main__':
    