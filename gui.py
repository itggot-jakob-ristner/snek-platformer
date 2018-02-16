import pygame as pg
from main import *
from settings import *



class Menutext:
    def __init__(self, text, screen, color, size=16, AA=True):
        self.font = pg.font.Font("resources/fonts/PressStart2P.ttf", size)
        self.screen_text = self.font.render(text, AA, color)
        self.screen = screen
        self.anti_aliasing = AA
        self.rect = self.screen_text.get_rect()
        self.color = color

    def draw(self, cord):
        self.screen.blit(self.screen_text, (cord))

    def update(self, new_text, color, newsize=16):
        self.font = pg.font.Font("resources/fonts/PressStart2P.ttf", newsize)
        self.screen_text = self.font.render(new_text, self.anti_aliasing, color)
        self.rect = self.screen_text.get_rect()

class Pausemenu:
    def __init__(self, game):
        self.game = game
        self.open = True
        self.player = self.game.player
        self.options = ["Inventory", "Map", "Save & Quit"]
        self.texts = []
        self.selected = 0
        self.background = pg.Surface((WIDTH, HEIGHT))
        self.background.set_alpha(180)
        self.background.fill(BLACK)
        for i in self.options:
            self.texts.append(Menutext(i, self.game.screen, (150, 150, 150), 32))
            
            
    def run(self):
        self.open = True
        while self.open:
            self.update()
            self.draw()
    
    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.open = False
                if self.game.playing:
                    self.game.playing = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_s or event.key == pg.K_DOWN:
                    if self.selected < len(self.options) - 1:
                        self.selected += 1
                elif event.key == pg.K_w or event.key == pg.K_UP:
                    if self.selected > 0:
                        self.selected -= 1
                elif event.key == pg.K_ESCAPE:
                    self.open = False

        
        for index, text in enumerate(self.texts):
            if index == self.selected:
                text.update(self.options[index], WHITE, 60)
            else:
                text.update(self.options[index], (150, 150, 150), 32)
            
            text.rect.center = (self.game.rect.centerx, index * 70 + 400)
           
    def draw(self):
        
        # Here we draw everything so give the visual of a frozen background
        self.game.draw()
        self.game.screen.blit(self.background, (0, 0))
        for index, text in enumerate(self.texts):
            text.draw(text.rect)
        self.game.clock.tick()
        pg.display.flip()

    def execute(self):
        self.selected.open()



class Healthbar:
    # The healthbar displayed in the top right
    def __init__(self, player):
        self.display_hp = player.hp
        self.display_max_hp = player.max_hp
        self.player = player
        self.game = player.game
        self.border = pg.Surface((self.display_max_hp * 3 + 6, 26))
        self.border.fill((210, 205, 42))
        self.border_rect = self.border.get_rect()
        self.background = pg.Surface((self.display_max_hp * 3, 20))
        self.background.fill(BLACK)
        self.hp_rect = pg.Surface((self.display_hp * 3, 20))
        self.hp_rect.fill((156, 39, 29))
        self.text = Menutext(f"HP:{self.player.hp} / {self.player.max_hp}", self.game.screen, YELLOW, 16)
    
    
    def update(self):
        # It crashes if you try to draw a rect with negative dimensions
        # and so we reset the hp if it dips below zero
        if self.player.hp <= 0:
            self.player.hp = 0
        self.text.update(f"HP:{self.player.hp} / {self.player.max_hp}", WHITE)
        if self.hp_rect.get_width() != self.player.hp * 3:
            self.hp_rect = pg.Surface((self.player.hp * 3, 20))
            self.hp_rect.fill((156, 39, 29))


    def draw(self):
        # Drawing the healthbar
        self.game.screen.blit(self.border, (20, 20))
        self.game.screen.blit(self.background, (23, 23))
        self.game.screen.blit(self.hp_rect, (23, 23))
        self.text.draw((20, 56))
