import pygame as pg
import sys
from settings import *
from sprites import *

class Game:
    def __init__(self):
        #---Initialize Game Window, etc---#
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    
    def new(self):
        #---Start a New Game
        self.all_sprites = pg.sprite.Group()
        self.run()
    
    def run(self):
        #---Game Loop--#
        self.playing = True
        while self.playing == True:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        #---Game Loop Update---#
        self.all_sprites.update()
    
    def events(self):
        #---Game Loop Events---#
        for event in pg.event.get():
            # Check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        #---Game Loop Draw---#
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)

        # After drawing everything we update the display with display.flip()
        pg.display.flip()
    
    def show_start_screen(self):
        #---Game Start / Splash Screen---#
        pass
    
    def show_go_screen(self):
        #---Game Over Screen---#
        pass

    

g = Game()
g.show_start_screen()
while g.running == True:
    g.new()
    g.show_go_screen()

pg.quit()

    


    