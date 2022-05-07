import pygame
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, height, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image_file).convert(), (width, height))
        self.rect = self.image.get_rect()

class Pause(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image =  pygame.transform.scale(pygame.image.load("images/pause2.png").convert_alpha(), (100 ,100))
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, 50)

class Health(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image =  pygame.transform.scale(pygame.image.load("images/ship.png").convert_alpha(), (100 ,100))
        self.rect = self.image.get_rect()
        self.rect.center = (width-150, 30)
        