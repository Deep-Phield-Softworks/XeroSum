#!/usr/bin/env python

# Generic item sheet object class


import pygame


class ItemSheet:
    # Constructor
    def __init__(self, image_key, image_path,
                 COLORKEY=pygame.Color('#0080ff')):
        self.image_key = image_key  # Image file name
        self.image_path = image_path
        self.surface = pygame.image.load(self.image_path)
        self.surface.set_colorkey(COLORKEY)

        self.frame_size_dict = dict()
        # Frame Size 'Cheat Sheet' dict
        # 420__pixel_art__icons_for_rpg_by_7soul1-d25c1np.png
        self.frame_size_dict['icons.png'] = {'frames_wide': 14,
                                             'frames_high': 30,
                                             'author': '7soul1-d25c1np'}
        # How many pixels wide is image
        self.pixels_wide = self.surface.get_width()
        # How many pixels high is image
        self.pixels_high = self.surface.get_height()
        # How many frames wide is image
        self.frames_wide = self.frame_size_dict[self.image_key]['frames_wide']
        # How many frames high is image
        self.frames_high = self.frame_size_dict[self.image_key]['frames_high']
        # One frame's width
        self.frame_width = self.pixels_wide/self.frames_wide
        # One frame's height
        self.frame_height = self.pixels_high/self.frames_high
        self.frames = []

    def populate_frames(self):
        for i in range(self.frames_high):
            self.frames.append(create_strip(i))

    '''
    Split a strip into a temp array of ordered subsurfaces
    for assignment in proper "animation order"
    '''
    def create_strip(self, row):
        top = self.frame_height * row
        left = 0  # Initially left has an x axis value of 0.
        strip = []
        # The bottom rows follow different rules than top rows
        for x in range(self.frames_wide):  # For each frame in the strip
            Rect = pygame.Rect((left, top), (self.frame_width, self.frame_height))
            frame = self.surface.subsurface(Rect)
            strip.append(frame)
            left += width  # Add width for each
        return strip
