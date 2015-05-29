#!/usr/bin/env python
import os


import pygame


from unboundmethods import TILE_WIDTH, TILE_HEIGHT
from spritesheet import SpriteSheet
from itemsheet import ItemSheet


pygame.init()
wide = pygame.display.Info().current_w
high = pygame.display.Info().current_h
screen_size = [wide, high]
COLORKEY = pygame.Color('#0080ff')
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
screen.set_colorkey(COLORKEY)

art_dir = os.path.join(os.getcwd(), 'pngs')
tile_dir = os.path.join(art_dir, 'tiles')
item_dir = os.path.join(art_dir, 'items')
sprite_dir = os.path.join(art_dir, 'sprites')
ui_dir = os.path.join(art_dir, 'ui')
tile_manifest = dict()
sprite_manifest = dict()
item_manifest = dict()
ui_manifest = dict()

for tile in os.listdir(tile_dir):
    # Make a tile_manifest entry with filename key and pygame.image value
    if '.png' in str(tile):
        path = os.path.join(tile_dir, tile)
        tile_manifest[str(tile)] = pygame.image.load(path).convert_alpha()
for sprite in os.listdir(sprite_dir):
    if '.png' in str(sprite):
        path = os.path.join(sprite_dir, sprite)
        sprite_manifest[str(sprite)] = SpriteSheet(sprite, path, 8, 4)
for item_sheet in os.listdir(item_dir):
    if '.png' in str(item_sheet):
        path = os.path.join(item_dir, item_sheet)
        item_manifest[str(item_sheet)] = ItemSheet(item_sheet,  path)
for ui_img in os.listdir(ui_dir):
    if '.png' in str(ui_img):
        path = os.path.join(ui_dir, ui_img)
        ui_manifest[str(ui_img)] = pygame.image.load(path)

pygame.mixer.init()
tracks = []
music_manifest = dict()
music_dir = os.getcwd() + os.sep + "sound" + os.sep + "music" + os.sep
for track in os.listdir(music_dir):
    music_manifest[str(track)] = str(music_dir) + str(track)
    tracks.append(str(music_dir) + str(track))

fx_manifest = dict()
fx_dir = os.getcwd() + os.sep + "sound" + os.sep + "FX" + os.sep
for fx in os.listdir(fx_dir):
    filename = str(fx_dir) + str(fx)
    sound = pygame.mixer.Sound(filename)
    key = fx.split('.')[0]
    fx_manifest[str(key)] = sound
