import pygame
import random
from math import pi, cos, sin


WIDTH = 1200
HEIGHT = 775
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load("ship2mod.png").convert()
        self.rect = self.image_orig.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed_x=0
        self.speed_y=0
        self.rot = 0
        self.image_orig.set_colorkey((128,128,128))

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rot += 5
        if keys[pygame.K_RIGHT]:
            self.rot -= 5
        if keys[pygame.K_DOWN]:
            self.speed_x = 0                   #-1*cos((self.rot % 360) * pi / 180) / 10
            self.speed_y = 0                    #sin((self.rot % 360) * pi / 180) / 10
        if keys[pygame.K_UP]:    
            self.speed_x += cos((self.rot % 360) * pi / 180 + pi / 2) 
            self.speed_y += -1*sin((self.rot % 360) * pi / 180 + pi / 2) 
        

        if self.rect.center[0] > WIDTH:
            self.rect.center = (0, self.rect.center[1])
        if self.rect.center[0] < 0:
            self.rect.center = (WIDTH, self.rect.center[1])
        if self.rect.center[1] > HEIGHT:
            self.rect.center = (self.rect.center[0], 0)
        if self.rect.center[1] < 0:
            self.rect.center = (self.rect.center[0], HEIGHT)

    
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
print(all_sprites.sprites())



running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Обновление
    all_sprites.update()
    # Рендеринг
    screen.fill(RED)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()