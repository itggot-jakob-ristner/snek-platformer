import pygame as pg
from settings import *


pg.init()
DISPLAY = pg.display.set_mode((WIDTH, HEIGHT))
game_done = False
clock = pg.time.Clock()

while not game_done:
    #---Main Event Loop---#
    for event in pg.event.get():
       if event.type == pg.QUIT:
           game_done = True
    

    display.fill(WHITE)

    #---Updating the Display---#
    pg.display.flip()
    clock.tick(FPS)
    