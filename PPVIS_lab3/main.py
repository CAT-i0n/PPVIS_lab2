import pygame
import pygame_menu
from background import Background
from player import Player
from asteroids import Asteroids
from pause import Pause
class Game:
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height         
        self.fps = fps
        self.count = 0

    def start(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ASSteroids")
        self.clock = pygame.time.Clock()
        menu = pygame_menu.Menu('', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)
        menu.add.button('Play', self.run_game)
        menu.add.button('Leaders', self.leaderBoard)
        menu.add.button('Exit', pygame.quit)
        menu.mainloop(self.screen)

    def leaderBoard(self):
        pass

    def add_record(self):
        loseBack = Background("images/youdied.png", self.height, self.width)
        while True:
            self.screen.blit(loseBack.image, loseBack.rect)

            font = pygame.font.Font(None, 200)
            count = font.render(str(self.count), True, (0, 255, 255))
            self.screen.blit(count,((self.width - count.get_rect().width)/2, 
                                        self.height * 0.65))

            font = pygame.font.Font(None, 100)
            count = font.render("press enter", True, (255, 255, 255))
            self.screen.blit(count,((self.width - count.get_rect().width)/2,
                                        self.height * 0.8))

            pygame.display.flip() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start()

    def run_game(self):
        
        pause = pygame.sprite.Group()
        pause.add(Pause(self.width))
        player = Player(self.width, self.height)
        asteroids = Asteroids(self.width, self.height)
        Back = Background("images/back.png", self.height, self.width)

        self.count = 0
        running = True
        while running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if 50 > ((self.width/2 - mouse[0])**2 + (50 - mouse[1])**2)**0.5:
                        isPause = True
                        while isPause:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse = pygame.mouse.get_pos()
                                    if 50 > ((self.width/2 - mouse[0])**2 + (50 - mouse[1])**2)**0.5:
                                        isPause = False

            player.update()
            asteroids.update()
            self.screen.fill((0, 0, 0))
            self.screen.blit(Back.image, Back.rect)

            asteroids.group.draw(self.screen)
            player.group.draw(self.screen)
            pause.draw(self.screen)
            font = pygame.font.Font(None, 60)
            count = font.render(str(self.count), True, (80, 0, 255, 255))
            self.screen.blit(count,(0,0))
            pygame.display.flip()  

            for asteroid in asteroids.items:
                if asteroid.rect.left < player.ship.rect.center[0] < asteroid.rect.right :
                        if asteroid.rect.top < player.ship.rect.center[1] < asteroid.rect.bottom :
                            self.add_record()



            for shot in player.ship.shots:
                for asteroid in asteroids.items:
                    if asteroid.rect.left + 5 < shot.rect.center[0] < asteroid.rect.right - 5:
                        if asteroid.rect.top + 5 < shot.rect.center[1] < asteroid.rect.bottom - 5:
                            if asteroid.size == 100:
                                self.count += 25
                            elif asteroid.size == 66:
                                self.count += 50
                            elif asteroid.size == 44:
                                self.count += 100
                            player.ship.shots.remove(shot)
                            asteroids.decay(asteroid)
                            asteroids.items.remove(asteroid)
                            break
            
        pygame.quit()       


if __name__ == "__main__":
    Game(1360, 765, 60).start()