import pygame as pg
from main import *

g = Game()
g.show_start_screen()
while g.running:
    g.new("start_map.tmx")
    g.show_go_screen()

pg.quit()