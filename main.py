import pygame as pg
import sys
from sprites import *
from settings import *



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
        #---Initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        p1 = Platform(0, HEIGHT - 40, WIDTH, 40)
        self.all_sprites.add(p1)
        self.platforms.add(p1)

        p2 = Platform(WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 80)
        self.all_sprites.add(p2)
        self.platforms.add(p2)

    
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
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

    def draw(self):
        #---Game Loop Draw---#
        self.screen.fill(BLACK)
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
    g.run()
    g.show_go_screen()

pg.quit()

    


    