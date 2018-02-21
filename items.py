import pygame as pg

class Item:
    def __init__(self, name, value, usable=True):
        self.name = name
        self.value = value
        self.usable = usable

class Consumable(Item):
    def __init__(self, name, value, deltaH):
        super().__init__(name, value)
        self.deltaH = deltaH
        self.equipabble = False
    
    def use(self, player):
        if player.hp != player.max_hp:
            player.hp += self.deltaH
            player.inventory.remove(self)

class Weapon(Item):
    def __init__(self, name, value, hitbox, damage, recovery):
        super().__init__(name, value)
        self.hitbox = pg.sprite.Sprite()
        self.hitbox.rect = pg.Rect(hitbox)
        self.equipabble = "weapon"
        self.damage = damage
        self.recovery = recovery
        

def generate_items():
    items = []
    small_h_pot = Consumable("Small Health Potion", 10, 20)
    items.append(Weapon("Epic Sword", 20, (0, 0, 200, 20), 50, 2))
    for i in range(2):
        items.append(small_h_pot)
    return items


    


