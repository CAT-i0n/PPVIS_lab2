import pygame
from background import Background
from player import Player
class Asteroids:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height         
        self.fps = fps

    def run(self):
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ASSteroids")
        clock = pygame.time.Clock()

        player = Player(self.width, self.height)

        Back = Background("images/back.png", self.height, self.width)

        running = True
        while running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            player.update()
            screen.fill((0, 0, 0))
            screen.blit(Back.image, Back.rect)
            player.group.draw(screen)
            pygame.display.flip()

        pygame.quit()       


if __name__ == "__main__":
    Asteroids(1360, 765, 60).run()