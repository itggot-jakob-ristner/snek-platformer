import pygame as pg
from settings import *
from os import path
vec = pg.math.Vector2

class Entity(pg.sprite.Sprite):
    # Superclass for all movinf entitys; players and enemies etc
    def __init__(self, game, x, y, groups, images, hp):
        self.groups = groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = vec(x, y)
        self.pos = vec(self.rect.x, self.rect.y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.hp = PLAYERHP
        self.max_hp = self.hp
        self.in_air = True
        self.facing = vec(0, 1)
    
    def jump(self):
        # jump only if standing on a platform
        if not self.in_air:
            self.vel.y = -25
            self.in_air = True
    
    def collide(self, direction, group):
        #This function makes the sprite not pass through other sprites
        hits = pg.sprite.spritecollide(self, group, False)
        hits = [x for x in hits if x != self]
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
            #self.in_air = False
    




class Player(Entity):
    def __init__(self, game, x, y):
        game_folder = path.dirname(__file__)
        recoures_folder = path.join(game_folder, "resources")
        player_models_folder = path.join(recoures_folder, "player_models")
        images = [pg.image.load(path.join(player_models_folder, "player_right.png")), pg.image.load(path.join(player_models_folder, "player_left.png"))]
        super().__init__(game, x, y, [game.obstacles, game.all_sprites], images, PLAYERHP)
        self.health_disp = Healthbar(self)
        self.inventory = []


    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
            self.image = self.images[1]
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
            self.image = self.images[0]
        if keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_r]:
            self.hp -= 1
        if self.vel.y < 0:
            self.in_air = True
        
        if self.vel.x > 0:
            self.facing = vec(0, 1)
        elif self.vel.x < 0:
            self.facing = vec(0, 1)
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # makes friction work both directions :P
        self.vel += self.acc
        d_x = int(self.vel.x + 0.5 * self.acc.x)
        d_y = int(self.vel.y + 0.5 * self.acc.y)
        self.pos.x += d_x * (self.game.dt / 20)
        self.pos.y += d_y * (self.game.dt / 20)
        #Checks collisions with obstacles
        self.rect.x = self.pos.x
        self.collide("x", self.game.obstacles) 
        self.rect.y = self.pos.y
        self.collide("y", self.game.obstacles)



class Npc(Entity):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, [game.obstacles, game.all_sprites, game.enemies], [pg.Surface((32, 64))], PLAYERHP)
        self.image.fill(RED)
        self.player = self.game.player

    
    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        direction = self.player.pos - self.pos

        if direction.x > 0:
            self.acc.x = NPCACC
        elif direction.x < 0:
            self.acc.x = -NPCACC
        if self.vel.y < 0:
            self.in_air = True
        
        self.rect.x += 1
        hits_right = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x -= 2
        hits_left = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x += 1
        if hits_right and self.vel.x > 0:
            self.jump()
        elif hits_left and self.vel.x < 0:
            self.jump()


        if self.vel.x > 0:
            self.facing = vec(0, 1)
        elif self.vel.x < 0:
            self.facing = vec(0, 1)

        self.acc.x += self.vel.x * NPCFRIC
        self.vel += self.acc
        d_x = int(self.vel.x + 0.5 * self.acc.x)
        d_y = int(self.vel.y + 0.5 * self.acc.y)
        self.pos.x += d_x * (self.game.dt / 20)
        self.pos.y += d_y * (self.game.dt / 20)
        self.rect.x = self.pos.x
        self.collide("x", self.game.obstacles) 
        self.rect.y = self.pos.y
        self.collide("y", self.game.obstacles)


class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, game):
        self.groups = [game.obstacles, game.walls]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

class Healthbar:
    def __init__(self, player):
        self.display_hp = player.hp
        self.display_max_hp = player.max_hp
        self.player = player
        self.game = player.game
        self.border_rect = pg.Surface((self.display_max_hp * 3 + 6, 26))
        self.border_rect.fill(WHITE)
        self.background = pg.Surface((self.display_max_hp * 3, 20))
        self.background.fill(RED)
        self.hp_rect = pg.Surface((self.display_hp * 3, 20))
        self.hp_rect.fill(GREEN)
        
    
    def update(self):
        if self.hp_rect.get_width() != self.player.hp * 3:
            self.hp_rect = pg.Surface((self.player.hp * 3, 20))
            self.hp_rect.fill(GREEN)


    def draw(self):
        self.game.screen.blit(self.border_rect, (20, 20))
        self.game.screen.blit(self.background, (23, 23))
        self.game.screen.blit(self.hp_rect, (23, 23))
        
        
        






    
        






































       