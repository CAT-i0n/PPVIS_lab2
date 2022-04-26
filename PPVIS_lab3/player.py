import pygame
from math import pi, cos, sin

class Flame(pygame.sprite.Sprite):
    def __init__(self, ship):
        self.ship = ship
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load("images/Flame_01.png").convert_alpha(), (250,250)), 
                       pygame.transform.scale(pygame.image.load("images/Flame_02.png").convert_alpha(), (250,250))]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.ship.rect.center[0], 
                            self.ship.rect.center[1] + 30)
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

class Ship(pygame.sprite.Sprite):
    def __init__(self, height, width):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image_orig = pygame.image.load("images/ship.png").convert_alpha()
        self.rect = self.image_orig.get_rect()
        self.rect.center = (self.width / 2, self.height / 2)
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

        if self.rect.center[0] > self.width:
            self.rect.center = (0, self.rect.center[1])
        if self.rect.center[0] < 0:
            self.rect.center = (self.width, self.rect.center[1])
        if self.rect.center[1] > self.height:
            self.rect.center = (self.rect.center[0], 0)
        if self.rect.center[1] < 0:
            self.rect.center = (self.rect.center[0], self.height)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center
        self.flame.update()



class Player:
    def __init__(self, height, width):
        self.group = pygame.sprite.Group()
        self.ship = Ship(height, width)
        self.group.add(self.ship)
    
    def update(self):
        if self.ship.is_move:
            self.group = pygame.sprite.Group()
            self.group.add(self.ship.flame)
            self.group.add(self.ship)
        else:
            self.group = pygame.sprite.Group()
            self.group.add(self.ship)
        self.group.update()