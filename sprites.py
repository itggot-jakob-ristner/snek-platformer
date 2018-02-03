import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = self.game.map.spawn
        self.pos = self.rect
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.in_air = True


    def jump(self):
        # jump only if standing on a platform
        if not self.in_air:
            self.vel.y = -25
            self.in_air = True


    def update(self):
        self.prev_pos = self.pos

        self.acc = vec(0, PLAYER_GRAV)

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
       
        # makes friction work both directions :P
        self.vel += self.acc
        d_x = int(self.vel.x + 0.5 * self.acc.x)
        d_y = int(self.vel.y + 0.5 * self.acc.y)

        self.pos.x += d_x * (self.game.dt / 20)
        self.pos.y += d_y * (self.game.dt / 20)

        #wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        # if self.rect.right > self.game.map_length:
        #     self.rect.right = self.game.map_length
        #     self.pos = vec(self.rect.x, self.rect.y)
        # elif self.rect.left < 0:
        #     self.rect.left = 0
        #     self.pos = vec(self.rect.x, self.rect.y)

        # print(self.rect.left)


        

        #Checks collisions with obstacles
        self.rect.x = self.pos.x
        self.collide("x") 
        self.rect.y = self.pos.y
        self.collide("y")

        #Checks if the player is on the ground
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if not hits:
            self.in_air = True
        self.rect.y -= 1


    def collide(self, direction):
        #This function makes the sprite not pass through other sprites
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            if direction == "y":
                if self.vel.y > 0:
                    self.rect.bottom = hits[0].rect.top
                    self.vel.y = 0
                    self.in_air = False
                    self.pos = vec(self.rect.x, self.rect.y)
                elif self.vel.y < 0:
                    self.rect.top = hits[0].rect.bottom
                    self.vel.y = 0
                    self.pos = vec(self.rect.x, self.rect.y)

            elif direction == "x":
                if self.vel.x > 0:
                    self.rect.right = hits[0].rect.left
                    self.vel.x = 0
                    self.pos = vec(self.rect.x, self.rect.y)
                if self.vel.x < 0:
                    self.rect.left = hits[0].rect.right 
                    self.vel.x = 0
                    self.pos = vec(self.rect.x, self.rect.y)
                self.in_air = False
        

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Map():
    def __init__(self, mapdata, game):
        self.tiles = mapdata[0]
        self.spawn = mapdata[1]
        self.game = game
        self.map_sprite = self.tiles[::-1]
        self.map_length = len(self.map_sprite[0])
        self.sprite = []
        index_y = HEIGHT - TILESIZE
        for y, line in enumerate(self.map_sprite):
            for x, letter in enumerate(line):
                if letter == "W":
                    self.sprite.append((x * TILESIZE, index_y  - y * TILESIZE, TILESIZE, TILESIZE, WHITE))
    
    def loadmap(self):
        for plat in self.sprite:
            p = Platform(*plat)
            self.game.all_sprites.add(p)
            self.game.platforms.add(p)


    
        






































       