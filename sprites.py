import pygame as pg
from settings import *
from os import path
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        game_folder = path.dirname(__file__)
        recoures_folder = path.join(game_folder, "resources")
        player_models_folder = path.join(recoures_folder, "player_models")
        self.img = path.join(player_models_folder, "player.png")
        self.image = pg.image.load(self.img)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
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
        self.acc = vec(0, PLAYER_GRAV)

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE]:
            self.jump()

        #Checks if the player is on the ground
        # self.rect.y += 1
        # hits = pg.sprite.spritecollide(self, self.game.obstacles, False)
        # if not hits:
        #     self.in_air = True
        # self.rect.y -= 1

        if self.vel.y < 0:
            self.in_air = True


        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
       
        # makes friction work both directions :P
        self.vel += self.acc
        d_x = int(self.vel.x + 0.5 * self.acc.x)
        d_y = int(self.vel.y + 0.5 * self.acc.y)

        self.prev_vel = vec(self.vel.x, self.vel.y)

        self.pos.x += d_x * (self.game.dt / 20)
        self.pos.y += d_y * (self.game.dt / 20)

        #Checks collisions with obstacles

        self.rect.x = self.pos.x
        self.collide("x", self.game.obstacles) 
        self.rect.y = self.pos.y
        self.collide("y", self.game.obstacles)



        #Allows the player tow walk onto small tiles
        if not self.in_air:
            if self.vel.x > 0:
                self.rect.y -= 1
                self.rect.x += 1
                hits = pg.sprite.spritecollide(self, self.game.obstacles, False)
                self.rect.y -= TILESIZE
                hits2 = pg.sprite.spritecollide(self, self.game.obstacles, False)
                self.rect.y += TILESIZE + 1
                self.rect.x -= 1

                if hits and not hits2:
                    self.rect.bottom = hits[0].rect.y
                    self.rect.x += 1
                    self.pos = vec(self.rect.x, self.rect.y)
                    self.vel.x += self.prev_vel.x

            elif self.vel.x < 0:
                self.rect.y -= 1
                self.rect.x -= 1
                hits = pg.sprite.spritecollide(self, self.game.obstacles, False)
                self.rect.y -= TILESIZE
                hits2 = pg.sprite.spritecollide(self, self.game.obstacles, False)
                self.rect.y += TILESIZE + 1
                self.rect.x += 1

                if hits and not hits2:
                    self.rect.bottom = hits[0].rect.y
                    self.rect.x -= 1
                    self.pos = vec(self.rect.x, self.rect.y)
                    self.vel.x += self.prev_vel.x





        
       


    def collide(self, direction, group):
        #This function makes the sprite not pass through other sprites
        hits = pg.sprite.spritecollide(self, group, False)
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
        

class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, game):
        self.groups = game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y





    
        






































       