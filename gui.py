import pygame as pg
from main import *


class Menutext:
    def __init__(self, text, screen, size=16, AA=True):
        self.font = pg.font.Font("resources/fonts/PressStart2P.ttf", size)
        self.screen_text = self.font.render(text, AA, BLACK)
        self.screen = screen
        self.anti_aliasing = AA
        self.rect = self.screen_text.get_rect()

    def draw(self, cord):
        self.screen.blit(self.screen_text, (cord))

    def update(self, new_text):
        self.screen_text = self.font.render(new_text, self.anti_aliasing, BLACK)
        self.rect = self.screen_text.get_rect()