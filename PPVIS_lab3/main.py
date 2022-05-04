import pygame
from background import Background
from player import Player
from asteroids import Asteroids
class Game:
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
        asteroids = Asteroids(self.width, self.height)
        Back = Background("images/back.png", self.height, self.width)

        running = True
        while running:
            clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            player.update()
            asteroids.update()
            screen.fill((0, 0, 0))
            screen.blit(Back.image, Back.rect)
            asteroids.group.draw(screen)
            player.group.draw(screen)
            pygame.display.flip()  
            for shot in player.ship.shots:
                for asteroid in asteroids.items:
                    if asteroid.rect.left + 5 < shot.rect.center[0] < asteroid.rect.right - 5:
                        if asteroid.rect.top + 5 < shot.rect.center[1] < asteroid.rect.bottom - 5:
                            player.ship.shots.remove(shot)
                            asteroids.decay(asteroid)
                            asteroids.items.remove(asteroid)
                            break

                        

        pygame.quit()       


if __name__ == "__main__":
    Game(1360, 765, 60).run()