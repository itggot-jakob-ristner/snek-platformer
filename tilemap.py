import pygame as pg
from settings import *
from sprites import *

class Map():
    def __init__(self, mapdata, game):
        self.tiles = mapdata[0]
        self.spawn = mapdata[1]
        self.game = game
        self.data = self.tiles[::-1]
        self.sprites = []
        index_y = HEIGHT - TILESIZE
        for y, line in enumerate(self.data):
            for x, letter in enumerate(line):
                if letter == "W":
                    self.sprites.append((x * TILESIZE, index_y  - y * TILESIZE, TILESIZE, TILESIZE, WHITE))

        self.tilewidth = len(self.tiles[0])
        self.tileheight = len(self.tiles) 
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        print(self.tilewidth, TILESIZE, self.width)



    def loadmap(self):
        for plat in self.sprites:
            p = Tile(*plat)
            self.game.all_sprites.add(p)
            self.game.tiles.add(p)
    

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        x = max(-(self.width - WIDTH), x)  # right
        # y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)