import pygame as pg
import random
import pytmx
from settings import *
from sprites import *
from tilemap import *
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


    def loadmap(self):
        game_folder = path.dirname(__file__)
        resources_folder = path.join(game_folder, "resources")
        map_folder = path.join(resources_folder, "maps")
        self.map = Tilemap(path.join(map_folder, "start_map.tmx"))
        #self.map = Tilemap(path.join(map_folder, "test_map.tmx"))
        self.map_img = self.map.make_map()
        self.maprect = self.map_img.get_rect()



    def new(self):
        # start a new game
        self.loadmap()
        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        for tileobject in self.map.tmxdata.objects:
            if tileobject.name == "wall":
                Obstacle(tileobject.x, tileobject.y, tileobject.width, tileobject.height, self)
            if tileobject.name == "player":
                self.player = Player(self, tileobject.x, tileobject.y)

        self.camera = Camera(self.map.width, self.map.height)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.camera.update(self.player)

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(WHITE)
        self.screen.blit(self.map_img, self.camera.applyrect(self.maprect))
        #self.all_sprites.draw(self.screen)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))


        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass 