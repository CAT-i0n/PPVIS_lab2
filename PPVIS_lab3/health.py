import pygame
class Health(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image =  pygame.transform.scale(pygame.image.load("images/ship.png").convert_alpha(), (100 ,100))
        self.rect = self.image.get_rect()
        self.rect.center = (width-150, 30)