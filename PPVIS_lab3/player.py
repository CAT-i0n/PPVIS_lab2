import pygame
from math import pi, cos, sin
from time import time
from abc import ABC

class ButtonPressCommand(ABC):
    def execute(self, ship):
        pass

class ButtonPressReturnCommand(ButtonPressCommand):
    def execute(self, ship):
        if time() - ship.last_shot > ship.shot_delay:
            if not pygame.mixer.Channel(1).get_busy():
                pygame.mixer.Channel(1).set_volume(0.05)
                pygame.mixer.Channel(1).play(
                pygame.mixer.Sound(r'sounds\fire.mp3'))
            ship.shots.append(Shot(ship))
            ship.last_shot = time()
            if ship.side == 1:
                ship.side = -1
            elif ship.side == -1:
                ship.side = 1

class ButtonPressWCommand(ButtonPressCommand):
    def execute(self, ship):
        ship.speed_x += cos((ship.rot % 360) * pi / 180 + pi / 2) / 10
        ship.speed_y += -1*sin((ship.rot % 360) * pi / 180 + pi / 2) / 10
        if (ship.speed_x ** 2 + ship.speed_y ** 2) ** 0.5 > ship.speed_limit:
            ship.speed_x *= ship.speed_limit / (ship.speed_x ** 2 + ship.speed_y ** 2)**0.5
            ship.speed_y *= ship.speed_limit / (ship.speed_x ** 2 + ship.speed_y ** 2)**0.5
        ship.is_move = True
        
class ButtonPressACommand(ButtonPressCommand):
    def execute(self, ship):
        ship.rot += 5

class ButtonPressDCommand(ButtonPressCommand):
    def execute(self, ship):
        ship.rot -= 5

class ButtonPressSpaceCommand(ButtonPressCommand):
    def execute(self, ship):
        if abs(ship.speed_y) < 1:
            ship.speed_y = 0
        else:
            ship.speed_y *= 0.95
        if abs(ship.speed_x) < 1:
            ship.speed_x = 0
        else:                                
            ship.speed_x *= 0.95

class Shot(pygame.sprite.Sprite):
    def __init__(self, ship):
        super().__init__()
        self.speed = ship.speed_limit * 1.2
        self.image = pygame.transform.rotate(
            pygame.image.load("images/shot.png"), ship.rot)
        self.image.set_colorkey((0, 0, 0))
        self.rot = ship.rot % 360
        self.rect = self.image.get_rect()
        self.rect.center = (ship.rect.center[0] - 40 * sin((self.rot) * pi / 180) - ship.side * 30 * cos((self.rot) * pi / 180),
                            ship.rect.center[1] - 40 * cos((self.rot) * pi / 180) + ship.side * 30 * sin((self.rot) * pi / 180))

    def update(self):
        self.rect.x += self.speed * cos((self.rot % 360) * pi / 180 + pi / 2)
        self.rect.y -= self.speed * sin((self.rot % 360) * pi / 180 + pi / 2)




class Flame(pygame.sprite.Sprite):
    def __init__(self, ship):
        self.ship = ship
        super().__init__()
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
        super().__init__()
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
        self.side = 1
        self.speed_limit = 10
        self.comands = {pygame.K_a : ButtonPressACommand(),
                        pygame.K_d : ButtonPressDCommand(),
                        pygame.K_w : ButtonPressWCommand(),
                        pygame.K_SPACE : ButtonPressSpaceCommand(),
                        pygame.K_RETURN : ButtonPressReturnCommand(),}

    def update(self):
        if not pygame.mixer.Channel(0).get_busy() and self.is_move:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(r'sounds\thrust.wav'))
        keys=pygame.key.get_pressed()
        self.is_move = False   
        for command in self.comands.keys():
            if keys[command]:
                self.comands[command].execute(self)

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
        self.group.empty()
        if self.ship.is_move:
            self.group.add(self.ship.flame)
        self.group.add(self.ship)
        for shot in self.ship.shots:
            if shot.rect.left > self.ship.width or shot.rect.right < 0:
                self.ship.shots.remove(shot)
                continue
            if shot.rect.top > self.ship.height or shot.rect.bottom < 0:
                self.ship.shots.remove(shot)
                continue
            self.group.add(shot)
        self.group.update()
