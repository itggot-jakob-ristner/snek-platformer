import pygame as pg
import random
import pytmx
from settings import *
from sprites import *
from tilemap import *
from gui import * 
from items import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.rect = self.screen.get_rect()
        self.items = generate_items()
        self.player_spawned = False


    def loadmap(self, mappath):
        # This loads the map, pretty self explanatory
        game_folder = path.dirname(__file__)
        resources_folder = path.join(game_folder, "resources")
        map_folder = path.join(resources_folder, "maps")
        self.map = Tilemap(path.join(map_folder, mappath))
        self.map_img = self.map.make_map()
        self.maprect = self.map_img.get_rect()

        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.damaging_on_coll = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.cell_linkers = pg.sprite.Group()


        # Adds objects in to the game based on the object layer in the .tmx file loaded
        for tileobject in self.map.tmxdata.objects:
            if tileobject.name == "wall":
                Obstacle(tileobject.x, tileobject.y, tileobject.width, tileobject.height, self)
            elif tileobject.name == "player" and not self.player_spawned:
                self.player_spawned = True
                self.player = Player(self, tileobject.x, tileobject.y)
            elif tileobject.name == "enemy":
                Npc(self, tileobject.x, tileobject.y)
            elif tileobject.name == "cell_load":
                Celllinker(tileobject.x, tileobject.y, tileobject.width, tileobject.height, self, tileobject.properties["cell_link"], [float(coord) for coord in tileobject.properties["cell_spawn"].split(",")])

        if self.player not in self.all_sprites:
            self.all_sprites.add(self.player)
            self.players.add(self.player)




    def new(self):
        # start a new game
        self.loadmap("start_map.tmx")
        
        self.pausemenu = Pausemenu(self)
        self.camera = Camera(self.map.width, self.map.height)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(120)
            self.events()
            self.update()
            self.draw()
            # After drawing everything we flip the dispkay
            pg.display.flip()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.camera.update(self.player)
        self.player.health_disp.update()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.pausemenu.run()
                elif event.key == pg.K_b:
                    self.pausemenu.run()
                elif event.key == pg.K_e:
                    if self.player.attack_timer * (self.dt / 20) > self.player.weapon.recovery:
                        self.player.attack()
                        #self.player.image = pg.transform.rotate(self.player.image, 5)
                # elif event.key == pg.K_g:
                #     self.new("start_map.tmx")
            elif event.type == pg.KEYUP:
                if event.key == pg.K_e:
                    self.player.attacking = False


    def draw(self):
        # Game Loop - draw
        self.screen.fill(WHITE)
        self.screen.blit(self.map_img, self.camera.applyrect(self.maprect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for enemy in self.enemies:
            # This draws the healthbars for the enemies
            hp_percent = enemy.hp / enemy.max_hp
            background_rect = pg.Rect(enemy.rect.left, enemy.rect.top - 10, enemy.rect.width, 5)
            health_rect = pg.Rect(enemy.rect.left, enemy.rect.top - 10, enemy.rect.width * hp_percent, 5)
            pg.draw.rect(self.screen, RED, self.camera.applyrect(background_rect))
            pg.draw.rect(self.screen, YELLOW, self.camera.applyrect(health_rect))
        if self.player.attacking:
            pg.draw.rect(self.screen, BLACK, self.camera.apply(self.player.weapon.hitbox))
        self.player.health_disp.draw()


    def show_start_screen(self):
        # game splash/start screen
        started = False
        while not started:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        started = True
            self.screen.fill(BLACK)    
            self.clock.tick()       
            pg.display.flip           

    def show_go_screen(self):
        # game over/continue
        self.running = False