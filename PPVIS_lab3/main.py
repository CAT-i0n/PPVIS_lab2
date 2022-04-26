import pygame
from background import Background
from player import Player

class Astoroids:
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

        player = Player(self.height, self.width)

        BackGround=Background("images/back.png")
        running = True
        while running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            player.update()
            screen.fill((0, 0, 0))
            screen.blit(BackGround.image, BackGround.rect)
            player.group.draw(screen)
            pygame.display.flip()

        pygame.quit()       


if __name__ == "__main__":
    Astoroids(1024, 600, 60).run()