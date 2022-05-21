import pygame
import pygame_menu
class View:
    def __init__(self, presenter):
        self.presenter = presenter
    

    def run(self):
        def update():
            Map = self.presenter.getMap()
            for x in range(size):
                for y in range(size):
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

        def addObject():
            pos = pygame_menu.Menu('', 200, 400,
                                theme=pygame_menu.themes.THEME_DARK,
                                )
            pos.mainloop(display)

        pygame.init()
        display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        clock = pygame.time.Clock()
        menu = pygame_menu.Menu('', pygame.display.Info().current_w,
                                pygame.display.Info().current_h,
                                theme=pygame_menu.themes.THEME_DARK,
                                columns=4,
                                rows=2
                                )
        table = menu.add.table()
        
        Map = self.presenter.getMap()
        size = len(Map)

        table.resize(width=60, height = 60)

        for i in range(size):
            row = list()
            for x in range(size):
                row.append(pygame_menu.widgets.Image("img/back.png", scale=(0.5, 0.5)))
            table.add_row(row, cell_align=pygame_menu.locals.ALIGN_CENTER, cell_border_width=0)


        menu.add.button("Next step", step)
        menu.add.button("Generate", generate)
        menu.add.button("Add predator", addObject)
        menu.add.button("Add herbivore")
        menu.add.button("Add plant")
        menu.add.button("Exit", quit)

        menu.mainloop(display, bgfun=update)



