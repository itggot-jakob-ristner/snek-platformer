import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((41, 41))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = True


    def jump(self):
        # jump only if standing on a platform
        if not self.jumping:
            self.vel.y = -20
            self.jumping = True

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
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.x = self.pos.x
        self.collide("x") 

        self.rect.y = self.pos.y
        self.collide("y")




        
         

    def collide(self, direction):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            if direction == "y":
                if self.vel.y > 0:
                    print("HIT TOP SIDE OF WALL")
                    self.rect.bottom = hits[0].rect.top
                    self.vel.y = 0
                    self.jumping = False
                    self.pos = vec(self.rect.x, self.rect.y)
                elif self.vel.y < 0:
                    print("HIT BOTTOM SIDE OF WALL")
                    self.rect.top = hits[0].rect.bottom
                    self.vel.y = 0
                    self.pos = vec(self.rect.x, self.rect.y)
            
            elif direction == "x":
                if self.vel.x > 0:
                    print("HIT LEFT SIDE OF WALL")
                    self.rect.right = hits[0].rect.left
                    self.vel.x = 0
                    self.pos = vec(self.rect.x, self.rect.y)
                if self.vel.x < 0:
                    print ("HIT RIGHT SIDE OF WALL")
                    self.rect.left = hits[0].rect.right
                    self.vel.x = 0
                    self.pos = vec(self.rect.x, self.rect.y)




    
    def collide2(self):
        for platform in self.game.platforms:
            if self.rect.colliderect(platform.rect):
               
                if self.vel.y > 0:
                    self.vel.y = 0
                    self.is_jumping = False
                    self.rect.bottom = platform.rect.top
                    self.pos = vec(self.rect.centerx, self.rect.centery)
                
            

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y