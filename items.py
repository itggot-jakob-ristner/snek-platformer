import pygame as pg

class Item:
    def __init__(self, name, value, usable=False):
        self.name = name
        self.value = value
        self.usable = usable
