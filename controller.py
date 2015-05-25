#!/usr/bin/env python
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP,  KEYDOWN,  KEYUP,  K_ESCAPE,  K_F1,  K_F2,  K_F3
import transaction

from unboundmethods import timestamp,  within

class Controller:
    
    def __init__(self, game):
        self.game = game
    
    def handle_event(self, event):
        if event.type == QUIT: #If the little x in the window was clicked...
            self.game.run = False
        if event.type == MOUSEBUTTONDOWN:
                self.mouse_click(event)
        if event.type == KEYDOWN:
                self.keyboard(event)
        if event.type == KEYUP:
                pass

    def keyboard(self, event):
        global screen_text    
        pressed_keys = pygame.key.get_pressed()
        #'ESCAPE' key is for exiting the game
        if pressed_keys[K_ESCAPE]:
            self.game.run = False
        #'K_F1' key to toggle music
        if pressed_keys[K_F1]:
            pygame.mixer.music.stop()
            self.game.db['play_music'] = not self.game.db['play_music']
            
        #'K_F2' key for screenshot. This saves it to timeString().png    
        if pressed_keys[K_F2]:
            try:
                filename = timestamp() + '.png'
                pygame.image.save((screen),filename)
                print "screenshot saved as " + filename
            except EnvironmentError as e:
                print "Error:",  e
        if pressed_keys[K_F3]:
            #Play random sound
            fx_manifest[random.choice(fx_manifest.keys())].play()
    
    #Seperates mouse clicks into left and right and then call their seperate fncs
    def mouse_click(self, event):
        if (event.button == 1) and (event.type == MOUSEBUTTONDOWN):
            self.mouse_left_click(event)
        if event.button == 3 and (event.type == MOUSEBUTTONDOWN):
            self.mouse_right_click(event)
    
    #This function is called when a left mouse click is passed
    def mouse_left_click(self, event):
        self.game.screen_text_top = []
        self.game.selected = None
        point = (event.pos[0],event.pos[1])
        collide_list = []
        selected_info = None
        for e in self.game.view.hit_box_list:
            if e[0].collidepoint(point):
                if within(e[0], point):
                    collide_list.append(e)
        if collide_list:
            for e in collide_list:
                info = [e[1].coordinate_key, e[1].name, 'float:' + str(e[1].float_offset), 'layer: ' + str(e[1].layer), 'px,py: ', e[1].pixel_offsets]
                self.game.screen_text_top.append(str(info))
                if hasattr(e[1], 'controllable') and e[1].controllable:
                    self.game.selected = e[1]
    
    def mouse_right_click(self, event):
        if self.game.selected:
            point = (event.pos[0],event.pos[1])
            for e in self.game.view.hit_box_list:
                if e[0].collidepoint(point):
                    if within(e[0], point):
                        if hasattr(e[1], 'pathable') and e[1].pathable:
                            self.game.path_target = e[1].parent_coordinate
