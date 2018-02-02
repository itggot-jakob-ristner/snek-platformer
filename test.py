import pygame as pg
vec = pg.math.Vector2

pg.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

WIDTH = 700
HEIGHT = 500

PLAYER_ACC = 0.5
PLAYER_FRIC = 0.05
PLAYER_GRAV = 0.2

SPEED = 5

screen = pg.display.set_mode((WIDTH, HEIGHT))

clock = pg.time.Clock()

running = True

all_sprites = pg.sprite.Group()
platforms = pg.sprite.Group()



class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vec(0, 0)
        all_sprites.add(self)
        platforms.add(self)

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.is_jumping = True
        all_sprites.add(self)

    def update(self):
        keys = pg.key.get_pressed()

        '''
        player.vel = vec(0, 0)
        if keys[pg.K_a]:
            player.vel.x = -SPEED
        if keys[pg.K_d]:
            player.vel.x = SPEED
        if keys[pg.K_s]:
            player.vel.y = SPEED
        if keys[pg.K_w]:
            player.vel.y = -SPEED
        player.pos += player.vel
        '''
        self.acc = vec(0, PLAYER_GRAV)
        #self.acc = vec(0,0)
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE]:
            if not self.is_jumping:
                self.vel.y = -20
                self.is_jumping = True


        self.acc.x += self.vel.x * -PLAYER_FRIC
        self.vel += self.acc
        #self.pos += self.vel + 0.5 * self.acc


        d_x = int(self.vel.x + 0.5 * self.acc.x)
        d_y = int(self.vel.y + 0.5 * self.acc.y)
        self.pos.x += d_x
        self.pos.y += d_y
        #self.center = self.pos

        self.rect.center = (int(self.pos.x), self.pos.y)
        self.collide_with_walls()

    def collide_with_walls(self):
       
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
               
                if self.vel.y > 0:
                    self.vel.y = 0
                    self.is_jumping = False
                    self.rect.bottom = platform.rect.top
                    self.pos = vec(self.rect.centerx, self.rect.centery)
      

Platform(0, 450, 700, 50)
Platform(300, 300, 30, 20)
player = Player(WIDTH / 2, HEIGHT / 2, 40, 40)

while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    player.update()


    screen.fill(BLACK)
    all_sprites.draw(screen)
    pg.display.flip()
    clock.tick(60)