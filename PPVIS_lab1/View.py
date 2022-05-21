import pygame
import pygame_menu
class View:
    def __init__(self, presenter):
        self.presenter = presenter
    

    def run(self):
        def update():
            Map = self.presenter.getMap()
            for x in range(self.size):
                for y in range(self.size):
                    if Map[x][y] == "Herbivore":
                        image = pygame_menu.baseimage.BaseImage("img/rabbit.png")
                        table.get_cell(x+1, y+1).set_image(image)
                    elif Map[x][y] == "Predator":
                        image = pygame_menu.baseimage.BaseImage("img/wolf.png").scale(0.5,0.5)
                        table.get_cell(x+1, y+1).set_image(image)
                    elif Map[x][y] == "Plant":
                        image = pygame_menu.baseimage.BaseImage("img/carrot.png")
                        table.get_cell(x+1, y+1).set_image(image)
                    elif Map[x][y] == "Ground":
                        image = pygame_menu.baseimage.BaseImage("img/back.png").scale(0.5, 0.5)
                        table.get_cell(x+1, y+1).set_image(image)

        def step():
            self.presenter.step()

        def generate():
            self.presenter.generate()

        def quit():
            self.presenter.save()
            menu.disable()

        def text_inputX(x):
            self.coordX = x

        def text_inputY(y):
            self.coordY = y


        def inputCoords(objectType):
            menu = pygame_menu.Menu('Print coordinates', 400, 400,
                                theme=pygame_menu.themes.THEME_DARK,
                                position = (5, 70))
            menu.add.text_input(title = "X: ", default = "0", onchange = text_inputX)
            menu.add.text_input(title = "Y: ", default = "0",onchange = text_inputY)
            menu.add.button("Exit", menu.disable)
            text_inputX("0")
            text_inputY("0")
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.Exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.coordX.isdigit() and self.coordY.isdigit():
                                if 0<=int(self.coordX)<=self.size and 0<=int(self.coordY)<=self.size:
                                    self.presenter.addObject(objectType, int(self.coordX), int(self.coordY))
                            return

                if menu.is_enabled():
                    menu.update(events)
                    menu.draw(self.display)

                pygame.display.update() 

        def addObject():
            menu = pygame_menu.Menu('Choose entity', 400, 400,
                                theme=pygame_menu.themes.THEME_DARK,
                                position = (5, 70))
            running = True
            menu.add.button("Herbivore", inputCoords, "Herbivore")
            menu.add.button("Predator", inputCoords, "Predator")
            menu.add.button("Plant", inputCoords, "Plant")
            menu.add.button("Exit")
            
            while running:
                events = pygame.event.get()
                if menu.is_enabled():
                    menu.update(events)
                    menu.draw(self.display)
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.Exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            return
                pygame.display.update() 


        pygame.init()
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        clock = pygame.time.Clock()
        menu = pygame_menu.Menu('', pygame.display.Info().current_w,
                                pygame.display.Info().current_h,
                                theme=pygame_menu.themes.THEME_DARK,
                                columns=2,
                                rows=4
                                )

        menu.add.button("Next step", step)
        menu.add.button("Generate", generate)
        menu.add.button("Add Object", addObject)
        menu.add.button("Exit", quit)

        table = menu.add.table()
        
        Map = self.presenter.getMap()
        self.size = len(Map)

        table.resize(width=60, height = 60)

        for i in range(self.size):
            row = list()
            for x in range(self.size):
                row.append(pygame_menu.widgets.Image("img/back.png", scale=(0.5, 0.5)))
            table.add_row(row, cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_width=1)
        menu.mainloop(self.display, bgfun=update)



