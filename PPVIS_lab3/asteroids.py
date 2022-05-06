import pygame
from random import randrange, choice
from math import sin, cos, pi
from copy import deepcopy, copy
from time import time
class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, size = 100):
        super().__init__()
        self.size = size
        self.width = width
        self.height = height
        self.image_orig = pygame.transform.scale(pygame.image.load(f"images/aster{randrange(1,9)}.png").convert_alpha(), (size,size))
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rot_speed = randrange(-4,5)
        self.rot = 0
        self.speed = randrange(2,5)
        self.angle = choice((randrange(30, 60), randrange(120, 150), randrange(210, 240),randrange(300, 330))) * pi / 180
    def changeImage(self, image):
        self.image_orig = image
    def update(self):
        self.old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center
        self.rot += self.rot_speed
        self.rect.x += self.speed * cos(self.angle)
        self.rect.y += self.speed * sin(self.angle)
        if self.rect.center[0] > self.width:
            self.rect.center = (0, self.rect.center[1])
        if self.rect.center[0] < 0:
            self.rect.center = (self.width, self.rect.center[1])
        if self.rect.center[1] > self.height:
            self.rect.center = (self.rect.center[0], 0)
        if self.rect.center[1] < 0:
            self.rect.center = (self.rect.center[0], self.height)


class Asteroids:
    def __init__(self, width, height):
        self.height = height
        self.width = width 
        self.group = pygame.sprite.Group()
        self.num = 6
        self.currentNum = 6
        self.items = []
        self.newAsteroidTime = 4
        self.decayTime = 0
        for _ in range(self.num):
            self.items.append(Asteroid(*self.randCoords(), 
                                       width, 
                                       height))
            self.group.add(self.items[-1])

    def randCoords(self):
        choiceX = (choice((randrange(100), randrange(self.width-100, self.width))), randrange(self.height))
        choiceY = (randrange(self.width), choice((randrange(100), randrange(self.height-100, self.height))))
        return choice((choiceX, choiceY))

    def decay(self, asteroid):
        if asteroid.size == 44:
            return 
        if asteroid.size == 100:
            self.currentNum-=1
            self.decayTime = time()
        small1 = Asteroid(*asteroid.rect.center, 
                                       self.width, 
                                       self.height,
                                       size = asteroid.size // 1.5)
        small1.changeImage(pygame.transform.scale(asteroid.image_orig, (asteroid.size // 1.5, asteroid.size // 1.5)))
        small2 = Asteroid(*asteroid.rect.center, 
                                       self.width, 
                                       self.height,
                                       size = asteroid.size // 1.5)
        small2.changeImage(pygame.transform.scale(asteroid.image_orig, (asteroid.size // 1.5, asteroid.size // 1.5)))    
        small1.angle = asteroid.angle - pi / 15
        self.items.append(small1)
        small2.angle = asteroid.angle + pi / 15
        self.items.append(small2)

    def update(self):
        self.group.empty()
        if time() - self.decayTime > self.newAsteroidTime and self.currentNum < self.num:
            self.items.append(Asteroid(*self.randCoords(), 
                                       self.width, 
                                       self.height))
            self.currentNum += 1
            self.decayTime = time()
        for item in self.items:
            self.group.add(item)
        self.group.update()

        
