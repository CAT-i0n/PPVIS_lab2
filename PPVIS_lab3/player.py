import pygame
from math import pi, cos, sin
from time import time

class Shot(pygame.sprite.Sprite):
    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.transform.rotate(pygame.image.load("images/shot.png"), ship.rot)
        self.image.set_colorkey((0,0,0))
        self.ship = ship
        self.rot = self.ship.rot
        self.rect = self.image.get_rect()
        self.rect.center = (self.ship.rect.center[0] + 40*cos((self.rot % 360) * pi / 180 + pi / 2), 
                            self.ship.rect.center[1] - 40*sin((self.rot % 360) * pi / 180 + pi / 2))

                        
        

    def update(self):
        self.rect.x += self.speed * cos((self.rot % 360) * pi / 180 + pi / 2)
        self.rect.y -= self.speed * sin((self.rot % 360) * pi / 180 + pi / 2)
        


        

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
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image_orig = pygame.image.load("images/ship.png").convert_alpha()
        self.rect = self.image_orig.get_rect()
        self.rect.center = (self.width / 2, self.height / 2)
        self.speed_x=0
        self.speed_y=0
        self.rot = 0
        self.flame = Flame(self)
        self.shots = []
        self.is_move = False
        self.last_shot = time()
        self.shot_delay = 0.3

    def update(self):
        keys=pygame.key.get_pressed()
        self.is_move = False   
        if keys[pygame.K_a]:  #left
            self.rot += 5
        if keys[pygame.K_d]:  #right
            self.rot -= 5
        if keys[pygame.K_s]:  #down
            if abs(self.speed_y) < 1:
                self.speed_y = 0
            else:
                self.speed_y *= 0.95
            if abs(self.speed_x) < 1:
                self.speed_x = 0
            else:                                
                self.speed_x *= 0.95  
        if keys[pygame.K_w]:  #up
            self.speed_x += cos((self.rot % 360) * pi / 180 + pi / 2) / 10
            self.speed_y += -1*sin((self.rot % 360) * pi / 180 + pi / 2) / 10
            self.is_move = True
        if keys[pygame.K_RETURN]:
            if time() - self.last_shot > self.shot_delay:
                self.shots.append(Shot(self))
                self.last_shot = time()

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
        if self.is_move:
            self.flame.update()



class Player:
    def __init__(self, height, width):
        self.group = pygame.sprite.Group()
        self.ship = Ship(height, width)
        self.group.add(self.ship)
    
    def update(self):
        self.group = pygame.sprite.Group()
        if self.ship.is_move:
            self.group.add(self.ship.flame)
            self.group.add(self.ship)
        else:
            self.group.add(self.ship)
        for shot in self.ship.shots:
            self.group.add(shot)
        self.group.update()