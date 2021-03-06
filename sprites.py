import pygame as pg
from settings import *
from os import path
from gui import * 
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
        self.facing = vec(1, 0)
        self.damage_counter = 0
        self.i_frame = False
        self.prev_vel = vec(0, 0)
        self.attacking = False
    
    def jump(self):
        # jump only if standing on a platform
        if not self.in_air:
            self.vel.y = -25
            self.in_air = True
    
    def kill(self):
        for group in self.groups:
            group.remove(self)
    
    def collide(self, direction, group):
        #This function makes the sprite not pass through other sprites in a group
        hits = pg.sprite.spritecollide(self, group, False)
        hits = [x for x in hits if x != self]
        if hits:
            if direction == "y":
                if self.vel.y > 0: # going down; colliding with top of rect
                    self.rect.bottom = hits[0].rect.top
                    self.vel.y = 0
                    self.in_air = False
                    self.pos = vec(self.rect.x, self.rect.y)
                elif self.vel.y < 0: # going upwards; colliding with bottom of rect
                    self.rect.top = hits[0].rect.bottom
                    self.vel.y = 0
                    self.pos = vec(self.rect.x, self.rect.y)
            elif direction == "x":
                if self.vel.x > 0: # going right; colliding with left of rect
                    self.rect.right = hits[0].rect.left
                    self.vel.x = 0
                    self.pos = vec(self.rect.x, self.rect.y)
                if self.vel.x < 0: # going left; colliding with right of rect
                    self.rect.left = hits[0].rect.right 
                    self.vel.x = 0
                    self.pos = vec(self.rect.x, self.rect.y)
            return [True, hits[0]]
        return [False]

    




class Player(Entity):
    # This is the player class, the one you control.
    def __init__(self, game, x, y):
        game_folder = path.dirname(__file__)
        recoures_folder = path.join(game_folder, "resources")
        player_models_folder = path.join(recoures_folder, "player_models")
        images = [pg.image.load(path.join(player_models_folder, "player_right.png")), pg.image.load(path.join(player_models_folder, "player_left.png"))]
        super().__init__(game, x, y, [game.players, game.all_sprites, game.obstacles], images, PLAYERHP)
        self.health_disp = Healthbar(self)
        self.inventory = []
        # Giving player some items, (TEMPORARY)
        self.inventory = self.game.items
        self.equip(self.inventory[0])

        self.attack_timer = 0


    def update(self):  
        print(self.pos)
        speed_multiplier = 1
        # this stops the game from continiung when you die
        if self.hp <= 0:
            self.game.playing = False

        # This gives your player "i-frames" ie invincible frames where you cannot take damage
        # so that damage doesnt stack on one collosion
        self.damage_counter += 1
        if self.damage_counter * (self.game.dt / 20) > 20: # self.game.dt / 20 makes all timing time based instead of frame based
            self.i_frame = False
        else: 
            self.i_frame = True
        
        self.attack_timer += 1

        # Resets the acceleration every tick
        self.acc = vec(0, PLAYER_GRAV)

        # Basic inputs; event loop for the player
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            # Switches the image when you move from left to right
            self.acc.x = -PLAYER_ACC
            self.image = self.images[1]
            self.facing.x = -1
        if keys[pg.K_d]:
            #-:-
            self.acc.x = PLAYER_ACC
            self.image = self.images[0]
            self.facing.x = 1
        if keys[pg.K_w] or keys[pg.K_SPACE]:
            self.jump()
        if keys[pg.K_r]:
            self.hp -= 1
        if keys[pg.K_e]:
            pass
        if keys[pg.K_LSHIFT]:
            speed_multiplier = 2
            # if self.attack_timer * (self.game.dt / 20) < self.weapon.recovery:
            #     self.attacking = True
            #     print(self.attack_timer)
        if keys[pg.K_h]:
            try:
                self.inventory[0].use(self)
            except:
                pass
        

        if self.vel.y < 0:
            self.in_air = True
    

        # Apply sprint
        self.acc.x *= speed_multiplier

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # apply acceleration to the velocity
        self.vel += self.acc * (self.game.dt / 20)

        # makes friction work both directions because of floating point errors in python
        d_x = int(self.vel.x + 0.5 * self.acc.x)
        d_y = int(self.vel.y + 0.5 * self.acc.y)
        self.pos.x += d_x * (self.game.dt / 20)
        self.pos.y += d_y * (self.game.dt / 20)

        self.prev_vel.x = self.vel.x
        # First check collisions in x
        self.rect.x = self.pos.x
        self.collide("x", self.game.obstacles) 

        # Then y collisions
        self.rect.y = self.pos.y
        # This damages the player when they land on top of a damaging sprite, gives them i-frames and bumps them up
        if self.collide("y", self.game.damaging_on_coll)[0] and not self.i_frame:
            self.hp -= 10
            self.damage_counter = 0
            self.vel.y = -10
        self.collide("y", self.game.obstacles)
        self.coll_cell_link()

        if self.facing.x > 0:
            self.weapon.hitbox.rect.midleft = self.rect.midright
        else:
            self.weapon.hitbox.rect.midright = self.rect.midleft

        if self.hp > self.max_hp:
            self.hp = self.max_hp
    
    def equip(self, weapon):
        if weapon.equipabble == "weapon":
            self.weapon = weapon
            self.inventory.remove(weapon)
        else:
            print("thats not a weapon kid")
    
    def attack(self):
        self.attacking = True
        hits = pg.sprite.spritecollide(self.weapon.hitbox, self.game.enemies, False)
        if hits:
            for enemy in hits:
                enemy.hp -= self.weapon.damage
                enemy.vel.x = 15 * self.facing.x
                enemy.vel.y = -5
        self.attack_timer = 0
    
    def coll_cell_link(self):
        hits = pg.sprite.spritecollide(self, self.game.cell_linkers, False)
        if hits:
            hits[0].switch_cell()
    
    def loaddata(self):
        pass
    



class Npc(Entity):
    # This will eventually be a superclass for all entitys that are not the player but currently is just the enemies
    def __init__(self, game, x, y):
        super().__init__(game, x, y, [game.obstacles, game.all_sprites, game.damaging_on_coll, game.enemies], [pg.Surface((32, 64))], PLAYERHP)
        self.image.fill(BLACK)
        self.player = self.game.player
        self.healthbar = pg.Surface((16, 5))
        self.healthbar_rect = self.healthbar.get_rect()


    
    def update(self):
        
        self.acc = vec(0, PLAYER_GRAV)

        # direction is a vector that will always point towards tha player
        direction = self.player.pos - self.pos

        # Use the direction vector to control the movement of tha enemies, will eventually add aggro range
        if direction.x > 0:
            self.acc.x = NPCACC
            self.facing.x = 1
        elif direction.x < 0:
            self.acc.x = -NPCACC
            self.facing.x = -1
        if self.vel.y < 0:
            self.in_air = True
        
        # This causes the enemy to jump if there is a wall between the enemy and player
        self.rect.x += 1
        hits_right = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x -= 2
        hits_left = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.x += 1
        if hits_right and self.vel.x > 0:
            self.jump()
        elif hits_left and self.vel.x < 0:
            self.jump()


        self.acc.x += self.vel.x * NPCFRIC
        self.vel += self.acc * (self.game.dt / 20)
        d_x = int(self.vel.x + 0.5 * self.acc.x)
        d_y = int(self.vel.y + 0.5 * self.acc.y)
        self.pos.x += d_x * (self.game.dt / 20)
        self.pos.y += d_y * (self.game.dt / 20)


       
        self.rect.x = self.pos.x

        # the damaging collisions in x are handled by the enemy, why does this work
        # better than just doing both in the player.update() you might ask? I DONT FUCKING KNOW
        coll = self.collide("x", self.game.players)
        if coll[0] and not self.player.i_frame:
            self.player.hp -= 10
            self.player.damage_counter = 0
            self.player.vel.x = self.facing.x * 10
        self.collide("x", self.game.obstacles) 

        self.rect.y = self.pos.y
        self.collide("y", self.game.obstacles)

        if self.hp <= 0:
            self.kill()

        

    


class Obstacle(pg.sprite.Sprite):
    # This is just the class for walls you run into
    def __init__(self, x, y, w, h, game):
        self.groups = [game.obstacles, game.walls]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

class Celllinker(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, game, linked_map, spawn_point):
        self.groups = [game.cell_linkers]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.linked_map = linked_map
        self.spawn_point = spawn_point
    
    def switch_cell(self):
        self.game.player.vel = vec(0, 0)
        # transition to be added
        self.game.loadmap(self.linked_map)
        self.game.player.pos = vec(self.spawn_point[0], self.spawn_point[1]) * TILESIZE
        self.game.player.rect.x, self.game.player.rect.y = self.game.player.pos.y, self.game.player.pos.x
        
        






    
        






































       