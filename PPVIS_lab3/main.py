import pygame
import pygame_menu
from sprites import Background, Pause, Health
from player import Player
from asteroids import Asteroids
import json
from time import time
class Game:
    def __init__(self, width, height, fps):
        with open("data.json") as file:
            self.scoreDict = json.load(file)
        self.width = width
        self.height = height         
        self.fps = fps
        self.count = 0
        self.player_name = ""
        self.health = 3
        self.invulnarabilityTime = 2
        self.deathTime = 0

    def start(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ASteroids")
        self.clock = pygame.time.Clock()
        menu = pygame_menu.Menu('', self.width, self.height,
                       theme=pygame_menu.themes.THEME_DARK,
                       onclose = self.Exit)
        menu.add.button('Play', self.run_game)
        menu.add.button('Leaders', self.leaderBoard)
        menu.add.button('Exit', self.Exit)
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.Exit()

            if menu.is_enabled():
                menu.update(events)
                menu.draw(self.screen)

            pygame.display.update() 


    def leaderBoard(self):
        menu = pygame_menu.Menu('Leaderboard', self.width, self.height,
                       theme=pygame_menu.themes.THEME_DARK)
        
        for record in reversed(sorted(self.scoreDict.items(), key = lambda x: x[1])):
            menu.add.button(record[0] + '-'*(30-len(record[0]+str(record[1]))) +  str(record[1]), None)
        menu.add.button('Return', self.start)
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.Exit()

            if menu.is_enabled():
                menu.update(events)
                menu.draw(self.screen)
            pygame.display.update() 
        
    def text_input(self, name):
        self.player_name = name

    def add_record(self):
        loseBack = Background("images/youdied.png", self.height, self.width)
        menu = pygame_menu.Menu('Enter your name', 400, 120,
                       theme=pygame_menu.themes.THEME_DARK,
                       position =  (50, 98))
        menu.add.text_input(title = "", onchange = self.text_input)
        while True:
            self.screen.blit(loseBack.image, loseBack.rect)

            font = pygame.font.Font(None, 200)
            count = font.render("Score: " + str(self.count), True, (128, 128, 128))
            self.screen.blit(count,((self.width - count.get_rect().width)/2, 
                                        self.height * 0.65))            
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.Exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print(self.player_name)
                        if len(self.player_name) > 2:
                            self.scoreDict[self.player_name] = self.count
                        self.start()

            if menu.is_enabled():
                menu.update(events)
                menu.draw(self.screen)

            pygame.display.update() 
            
    def pause(self):
        isPause = True
        while isPause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Exit() 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if 50 > ((self.width/2 - mouse[0])**2 + (50 - mouse[1])**2)**0.5:
                        isPause = False

    def run_game(self):
        frame = 0
        self.player_name = ""
        self.health = 3
        status = pygame.sprite.Group()
        pauseIcon = Pause(self.width)
        status.add(pauseIcon)
        status.add(Health(self.width))
        player = Player(self.width, self.height)
        asteroids = Asteroids(self.width, self.height)
        Back = Background("images/back.png", self.height, self.width)

        self.count = 0
        running = True
        while running:
            self.clock.tick(self.fps)
            frame += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if pauseIcon.rect.width / 2 > ((self.width/2 - mouse[0])**2 + (pauseIcon.rect.width / 2 - mouse[1])**2)**0.5:
                        self.pause()

            player.update()
            asteroids.update()
            self.screen.fill((0, 0, 0))
            self.screen.blit(Back.image, Back.rect)

            asteroids.group.draw(self.screen)

            if time() - self.deathTime > self.invulnarabilityTime:
                player.group.draw(self.screen)
            else:
                if frame%2:
                    player.group.draw(self.screen)

            status.draw(self.screen)


            font = pygame.font.Font(None, 60)
            count = font.render("Score: "+str(self.count), True, (80, 0, 255, 255))
            self.screen.blit(count,(0,0))

            font = pygame.font.Font(None, 80)
            count = font.render(" X "+ str(self.health), True, (80, 0, 255, 255))
            self.screen.blit(count,(self.width - 110, 0))

            pygame.display.flip()  

            for asteroid in asteroids.items:
                if asteroid.rect.left < player.ship.rect.center[0] < asteroid.rect.right:
                        if asteroid.rect.top < player.ship.rect.center[1] < asteroid.rect.bottom:
                            if time() - self.deathTime > self.invulnarabilityTime:
                                self.deathTime = time()
                                if self.health == 1:
                                    self.add_record()
                                else:
                                    self.health -= 1
                                    player = Player(self.width, self.height)
                                    asteroids.decay(asteroid)
                                    asteroids.items.remove(asteroid)

            for shot in player.ship.shots:
                for asteroid in asteroids.items:
                    if asteroid.rect.left + 5 < shot.rect.center[0] < asteroid.rect.right - 5:
                        if asteroid.rect.top + 5 < shot.rect.center[1] < asteroid.rect.bottom - 5:
                            if asteroid.size == 100:
                                self.count += 25
                            elif asteroid.size == 66:
                                self.count += 37
                            elif asteroid.size == 44:
                                self.count += 56
                            player.ship.shots.remove(shot)
                            asteroids.decay(asteroid)
                            asteroids.items.remove(asteroid)
                            break
            
        self.Exit()  

    def Exit(self):
        with open("data.json", "w") as file:
            json.dump(self.scoreDict, file)
        pygame.quit()

if __name__ == "__main__":
    Game(1360, 765, 60).start()