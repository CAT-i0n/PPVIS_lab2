import pygame
class Pause(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image =  pygame.transform.scale(pygame.image.load("images/pause2.png").convert_alpha(), (100 ,100))
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, 50)
