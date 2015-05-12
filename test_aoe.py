#!/usr/bin/env python

from aoe import *
from unboundmethods import make_key
import unittest

class TestAoETemplates(unittest.TestCase):
    #Initialize test environmental variables and objects
    def setUp(self):
        self.origin_key = make_key([0,0,0])
        self.sq1 = Square(self.origin_key, [3,2])
        self.sq2 = Square(self.origin_key, [3,2], True)
        self.sq3 = Square(self.origin_key, 2)
        self.sq4 = Square(self.origin_key, 2, True)
        self.nD1 = make_n_dimension(6)
        self.nD2 = make_n_dimension([3,4])
        self.nD3 = make_n_dimension([2,3,4])
        self.cube1 = Cube(self.origin_key, [2,3,4])
        self.cube2 = Cube(self.origin_key, [2,3,4], True)
        self.cube3 = Cube(self.origin_key, 3)
        self.cube4 = Cube(self.origin_key, 2, True)
    
    #Test that keys are produced as expected
    def test_make_key(self):
        expected_key = '0_0_0'
        self.assertTrue(self.origin_key == expected_key)
    
    #Exercise the areaKeyList of the 4 test Squares
    def test_SquareAreas(self):
        sq1ExpectedArea = (self.sq1.magnitude[0]*2 + 1) * (self.sq1.magnitude[1]*2 + 1)
        self.assertTrue(len(self.sq1.areaKeyList) == sq1ExpectedArea)
        sq2ExpectedArea = self.sq2.magnitude[0] * self.sq2.magnitude[1]
        self.assertTrue(len(self.sq2.areaKeyList) == sq2ExpectedArea)
        sq3ExpectedArea = (self.sq3.magnitude * 2 + 1) * (self.sq3.magnitude * 2 + 1)
        self.assertTrue(len(self.sq3.areaKeyList) == sq3ExpectedArea)
        sq4ExpectedArea = self.sq4.magnitude * self.sq4.magnitude
        self.assertTrue(len(self.sq4.areaKeyList) == sq4ExpectedArea)
        self.assertTrue(len(self.sq1.areaKeyList) > len(self.sq2.areaKeyList))
        self.assertTrue(len(self.sq3.areaKeyList) > len(self.sq4.areaKeyList))
    
    #Exercise n Dimensional arrays of 2D and 3D
    def test_nDimensionalArray(self):
        self.assertTrue(len(self.nD1) == 6)
        self.assertTrue(len(self.nD2) == 3)
        for x in self.nD2:
            self.assertTrue(len(x) == 4)
        self.assertTrue(len(self.nD3) == 2)
        for y in self.nD3:
            self.assertTrue(len(y) == 3)
            for z in y:
                self.assertTrue(len(z) == 4)
    
    #Test shape of squares' nDimensionalArray 
    def test_SquareDimensionalArray(self):
        sq1Expected = [ ['-3_-2_0','-3_-1_0','-3_0_0','-3_1_0','-3_2_0'],
                        ['-2_-2_0','-2_-1_0','-2_0_0','-2_1_0', '-2_2_0'],
                        ['-1_-2_0','-1_-1_0','-1_0_0','-1_1_0', '-1_2_0'],
                        ['0_-2_0', '0_-1_0', '0_0_0', '0_1_0',  '0_2_0'],
                        ['1_-2_0', '1_-1_0', '1_0_0', '1_1_0',  '1_2_0'],
                        ['2_-2_0', '2_-1_0', '2_0_0', '2_1_0',  '2_2_0'],
                        ['3_-2_0', '3_-1_0', '3_0_0', '3_1_0',  '3_2_0'] ]
        cx, cy = 0, 0
        for x in sq1Expected:
            cy = 0
            for y in x:
                self.assertTrue(y == self.sq1.nDimensionalArray[cx][cy])
                cy += 1
            cx += 1    
        sq2Expected = [ ['0_0_0','0_1_0'],
                        ['1_0_0','1_1_0'],
                        ['2_0_0','2_1_0'] ]
        cx, cy = 0, 0
        for x in sq2Expected:
            cy = 0
            for y in x:
                self.assertTrue(y == self.sq2.nDimensionalArray[cx][cy])
                cy += 1
            cx += 1
        sq3Expected = [ ['-2_-2_0','-2_-1_0','-2_0_0','-2_1_0', '-2_2_0'],
                        ['-1_-2_0','-1_-1_0','-1_0_0','-1_1_0', '-1_2_0'],
                        ['0_-2_0', '0_-1_0', '0_0_0', '0_1_0',  '0_2_0'],
                        ['1_-2_0', '1_-1_0', '1_0_0', '1_1_0',  '1_2_0'],
                        ['2_-2_0', '2_-1_0', '2_0_0', '2_1_0',  '2_2_0'] ]
        cx, cy = 0, 0
        for x in sq3Expected:
            cy = 0
            for y in x:
                self.assertTrue(y == self.sq3.nDimensionalArray[cx][cy])
                cy += 1
            cx += 1
        sq4Expected = [ ['0_0_0','0_1_0'],
                        ['1_0_0','1_1_0'] ]
        cx, cy = 0, 0
        for x in sq4Expected:
            cy = 0
            for y in x:
                self.assertTrue(y == self.sq4.nDimensionalArray[cx][cy])
                cy += 1
            cx += 1
    
if __name__ == '__main__':
    unittest.main()
