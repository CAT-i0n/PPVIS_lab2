import pygame
import random
from math import pi, cos, sin



WIDTH = 1024
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASSteroids")
clock = pygame.time.Clock()

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()

class Flame(pygame.sprite.Sprite):
    def __init__(self, ship):
        self.ship = ship
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load("Flame_01.png").convert_alpha(), (250,250)), 
                       pygame.transform.scale(pygame.image.load("Flame_02.png").convert_alpha(), (250,250))]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rot = 0
        self.frame = 0
        self.image_num = 0
        self.image_orig = self.images[0]

    def update(self):
        self.frame+=1
        if not self.frame%5:   
            self.image_num +=1
            self.image_orig = self.images[self.image_num % 2]
        self.rot = self.ship.rot
        self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = (self.ship.rect.center[0] + -30*cos((self.rot % 360) * pi / 180 + pi / 2), 
                            self.ship.rect.center[1] + 30*sin((self.rot % 360) * pi / 180 + pi / 2))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load("ship.png").convert_alpha()
        self.rect = self.image_orig.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed_x=0
        self.speed_y=0
        self.rot = 0
        self.flame=Flame(self)
        self.is_move = False

    def update(self):
        keys=pygame.key.get_pressed()
        self.is_move = False   
        if keys[pygame.K_LEFT]:
            self.rot += 5
        if keys[pygame.K_RIGHT]:
            self.rot -= 5
        if keys[pygame.K_DOWN]:
            if abs(self.speed_y) < 1:
                self.speed_y = 0
            else:
                self.speed_y *= 0.95
            if abs(self.speed_x) < 1:
                self.speed_x = 0
            else:                                
                self.speed_x *= 0.95  
         
        if keys[pygame.K_UP]:    
            self.speed_x += cos((self.rot % 360) * pi / 180 + pi / 2) / 5
            self.speed_y += -1*sin((self.rot % 360) * pi / 180 + pi / 2) / 5
            self.is_move = True

        if self.rect.center[0] > WIDTH:
            self.rect.center = (0, self.rect.center[1])
        if self.rect.center[0] < 0:
            self.rect.center = (WIDTH, self.rect.center[1])
        if self.rect.center[1] > HEIGHT:
            self.rect.center = (self.rect.center[0], 0)
        if self.rect.center[1] < 0:
            self.rect.center = (self.rect.center[0], HEIGHT)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center
        self.flame.update()

    
all_sprites = pygame.sprite.Group()
flame = pygame.sprite.Group()
player = Player()

flame.add(player.flame)
all_sprites.add(player)

BackGround=Background("back.png")
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    


    # Обновление
    #all_sprites.update()
    player.update()
    # Рендеринг
    screen.fill(BLACK)
    screen.blit(BackGround.image, BackGround.rect)
    if player.is_move:
        flame.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()