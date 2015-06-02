#!/usr/bin/env python
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.locals import KEYDOWN,  KEYUP,  K_ESCAPE,  K_F1,  K_F2,  K_F3
import transaction

from unboundmethods import timestamp,  within


class Controller:

    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        if event.type == QUIT:
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
        if pressed_keys[K_ESCAPE]:
            self.game.run = False
        if pressed_keys[K_F1]:
            pygame.mixer.music.stop()
            key = 'play_music'
            value = not self.game.db['play_music']
            self.game.db_event(key, value)
        if pressed_keys[K_F2]:
            try:
                filename = timestamp() + '.png'
                pygame.image.save((screen), filename)
                print "screenshot saved as " + filename
            except EnvironmentError as e:
                print "Error:",  e
        if pressed_keys[K_F3]:
            fx_manifest[random.choice(fx_manifest.keys())].play()

    def mouse_click(self, event):
        if (event.button == 1) and (event.type == MOUSEBUTTONDOWN):
            self.mouse_left_click(event)
        if event.button == 3 and (event.type == MOUSEBUTTONDOWN):
            self.mouse_right_click(event)

    def mouse_left_click(self, event):
        self.game.screen_text_top = []
        self.game.selected = None
        point = (event.pos[0], event.pos[1])
        collide_list = []
        selected_info = None
        for e in self.game.view.rects:
            if e[0].collidepoint(point):
                if within(e[0], point):
                    collide_list.append(e)
        if collide_list:
            for e in collide_list:
                info = []
                info.append(str(e[1].coordinate_key))
                info.append(str(e[1].name))
                info.append(str('float:' + str(e[1].float_offset)))
                info.append(str('layer: ' + str(e[1].layer)))
                info.append(str('px,py: ', str(e[1].pixel_offsets)))
                self.game.screen_text_top.append(str(info))
                if hasattr(e[1], 'controllable') and e[1].controllable:
                    self.game.selected = e[1]

    def mouse_right_click(self, event):
        if self.game.selected:
            point = (event.pos[0], event.pos[1])
            for e in self.game.view.hit_box_list:
                if e[0].collidepoint(point):
                    if within(e[0], point):
                        if hasattr(e[1], 'pathable') and e[1].pathable:
                            self.game.path_target = e[1].parent_coordinate
