import pygame
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, height, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(image_file).convert(), (width, height))
        self.rect = self.image.get_rect()

        