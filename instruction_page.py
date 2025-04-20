try:
    import sys
    import pygame
    import utils
    from global_vars import BACKGROUND_COLOR, UPPER_TEXT
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print(f"couldn't load module. {err}")
    print("with love, instruction_page.py")
    sys.exit(2)

class Instructions(pygame.Surface) :
    """An instruction page"""
    def __init__(self, screen_size: tuple, text: list) :
        pygame.Surface.__init__(self, screen_size)
        self.convert()
        self.fill(BACKGROUND_COLOR)         
        utils.render_text(text, self, UPPER_TEXT)