#---Sprite Classes for the Game---#
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.binary = 1
        self.is_jumping = True
        self.prev_pos = self.pos
    def jump(self):
        # Jump only if standing on something
        if not self.is_jumping:
            self.is_jumping = True
            self.vel.y = -20

    def update(self):
        self.on_ground = True
        self.binary = 1
        self.prev_pos = self.pos


        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC

        # Applying friction
        self.acc.x += self.vel.x * PLAYER_FRIC
        # Equations of motion
        self.vel += self.acc

        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.collide_with_wall("y")

        self.pos.x += self.vel.x + 0.5 * self.acc.x
        self.collide_with_wall("x")
        self.rect.center = (int(self.pos.x), self.pos.y)

        self.rect.center = self.pos











    def collide_with_wall(self, direction):
        for platform in self.game.platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel.y > 0:
                    self.vel.y = 0
                    self.is_jumping = False
                    self.rect.bottom = platform.rect.top
                    self.pos = vec(self.rect.centerx, self.rect.centery)








        # hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        # if hits:
        #     self.rect.bottom = hits[0].rect.top
        #     self.vel.y = 0
