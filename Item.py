#!/usr/bin/env python
from Matter import Matter
#Items are objects that can be placed into inventory. They are:
#-unable to move themselves(usually)
#-movable from ground to inventory
#-may be usable
#-may be consumable
#Example: gun or loaf of bread
class Item(Matter):
    def __init__(self, imageKey, name = None, tall = 0, floatOffset = [0.5,0.5]):
        Matter.__init__(self, imageKey, name)
        self.tall = tall
        self.floatOffset = floatOffset
    def TICK(self, TICK):
        pass #Default items do nothing on Tick