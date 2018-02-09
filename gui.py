import pygame as pg
from main import *



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

    def update(self, new_text, color):
        self.screen_text = self.font.render(new_text, self.anti_aliasing, color)
        self.rect = self.screen_text.get_rect()



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