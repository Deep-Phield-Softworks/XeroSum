#!/usr/bin/env python
#Imports
import pygame, sys
from AoE import *
from World import World
from WorldView import WorldView
#Pygame display initialization
pygame.init()
SCREEN_SIZE = [pygame.display.Info().current_w, pygame.display.Info().current_h]
SCREEN = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
#World initialization
WORLD = World("DEMO")
originKey = '0_0_0'
cubeargs = {'origin': originKey, 'magnitude': [10,10,0], 'towardsNegInf': False}
shape = Cube(**cubeargs)
VIEW = WorldView(WORLD, shape, SCREEN_SIZE)
#Fill active chunks in VIEW with terrain
baseTerrain = {'imageKey': 'grass.png'}
rocks = {'imageKey':'rocks.png', 'speedModifier': 1.25, 'layer': 1.0}
bushes = {'imageKey': 'bush.png', 'speedModifier': 1.50, 'layer': 1.1}
for key in sorted(WORLD.active.keys()):
        WORLD.baseTerrainChunkFill(key, **baseTerrain)
        WORLD.randomFillChunkFeature(key, **rocks)
        WORLD.randomFillChunkFeature(key, **bushes)
#Render the VIEW now that there is somethign to see
VIEW.render()
SCREEN.blit(VIEW.surface, (0,0))
pygame.display.flip()
#Main control loop
while True:
    for event in pygame.event.get():#Go through all events
        if event.type == pygame.QUIT: #If the little x in the window was clicked...
            WORLD.close()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_ESCAPE]:
                WORLD.close()
                sys.exit()