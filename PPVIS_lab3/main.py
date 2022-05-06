from ast import While
import pygame
import pygame_menu
from background import Background
from player import Player
from asteroids import Asteroids
from pause import Pause
import json
class Game:
    def __init__(self, width, height, fps):
        with open("data.json") as f:
            self.scoreDict = json.load(f)
        self.width = width
        self.height = height         
        self.fps = fps
        self.count = 0
        self.player_name = ""

    def start(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ASSteroids")
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
        self.player = name

    def add_record(self):
        loseBack = Background("images/youdied.png", self.height, self.width)
        menu = pygame_menu.Menu('Enter your name', 400, 120,
                       theme=pygame_menu.themes.THEME_DARK,
                       position =  (50, 98))
        menu.add.text_input(title = "", onchange = self.text_input)
        while True:
            self.screen.blit(loseBack.image, loseBack.rect)

            font = pygame.font.Font(None, 200)
            count = font.render("Score: " + str(self.count), True, (0, 255, 255))
            self.screen.blit(count,((self.width - count.get_rect().width)/2, 
                                        self.height * 0.65))            
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.Exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(self.player_name) > 2:
                            self.scoreDict[self.player_name] = self.count
                        self.start()

            if menu.is_enabled():
                menu.update(events)
                menu.draw(self.screen)

            pygame.display.update() 
            

    def run_game(self):
        self.player_name = ""
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
                                    self.Exit() 
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
                                self.count += 37
                            elif asteroid.size == 44:
                                self.count += 56
                            player.ship.shots.remove(shot)
                            asteroids.decay(asteroid)
                            asteroids.items.remove(asteroid)
                            break
            
        self.Exit()  

    def Exit(self):
        print(self.scoreDict)
        with open("data.json", "w") as f:
            json.dump(self.scoreDict, f)
        pygame.quit()

if __name__ == "__main__":
    Game(1360, 765, 60).start()