import pygame
import pygame_menu
class View:
    def __init__(self, presenter) -> None:
        self.presenter = presenter
        self._running: bool = False

    def run(self) -> None:
        def update() -> None:
            Map: list = self.presenter.getMap()
            for x in range(self._size):
                for y in range(self._size):
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

        def step() -> None:
            self.presenter.step()

        def generate() -> None:
            self.presenter.generate()

        def quit() -> None:
            self.presenter.save()
            menu.disable()

        def text_inputX(x: str) -> None:
            self._coordX = int(x)

        def text_inputY(y: str) -> None:
            self._coordY = int(y)


        def inputCoords(objectType) -> None:
            menu = pygame_menu.Menu('Print coordinates', 400, 400,
                                theme=pygame_menu.themes.THEME_DARK,
                                position = (5, 70))
            valid_chars = [str(i) for i in range(10)]
            menu.add.text_input(title = "X: ", 
                                default = "0", 
                                onchange = text_inputX, 
                                valid_chars= valid_chars)
            menu.add.text_input(title = "Y: ", 
                                default = "0",
                                onchange = text_inputY,
                                valid_chars= valid_chars)
            menu.add.button("Exit")
            text_inputX("0")
            text_inputY("0")
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        self.Exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if 0<=self._coordX<=self._size and 0<=self._coordY<=self._size:
                                self.presenter.addObject(objectType, self._coordX, self._coordY)
                            return

                if menu.is_enabled():
                    menu.update(events)
                    menu.draw(self.display)

                pygame.display.update() 

        def addObject() -> None:
            menu = pygame_menu.Menu('Choose entity', 400, 400,
                                theme=pygame_menu.themes.THEME_DARK,
                                position = (5, 70))
            def stop():
                self._running = False
            menu.add.button("Herbivore", inputCoords, "Herbivore")
            menu.add.button("Predator", inputCoords, "Predator")
            menu.add.button("Plant", inputCoords, "Plant")
            menu.add.button("Exit", stop) 
            while self._running:
                events = pygame.event.get()
                if menu.is_enabled():
                    menu.update(events)
                    menu.draw(self.display)
                for event in events:
                    if event.type == pygame.QUIT:
                        self.Exit()
                pygame.display.update() 
            self._running = True


        pygame.init()
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        clock = pygame.time.Clock()
        menu = pygame_menu.Menu('Animal world', pygame.display.Info().current_w,
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
        
        Map: list = self.presenter.getMap()
        self._size: int = len(Map)

        table.resize(width=60, height = 60)

        for i in range(self._size):
            row = list()
            for x in range(self._size):
                row.append(pygame_menu.widgets.Image("img/back.png", scale=(0.5, 0.5)))
            table.add_row(row, cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_width=1)
        menu.mainloop(self.display, bgfun=update)



