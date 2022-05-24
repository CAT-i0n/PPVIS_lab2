import pygame_menu
import pygame

class MenuTheme(pygame_menu.Theme):
    def __init__(self) -> None:
        super().__init__()
        self.background_color = pygame.Color((0,0,0,0))
        self.widget_font = pygame_menu.font.FONT_8BIT
        self.widget_font_color = (0,0,255,0)
        self.widget_border_color = (0,0,0,0)
        #self.title_font_size = 
        #self.title_font = 
        self.title_font_color = (0,0,0,0)
        #self.widget_font_size = 
        self.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE

