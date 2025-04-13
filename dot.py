try:
    import sys
    import pygame
    from socket import *
    from pygame.locals import *
    from global_vars import DOT_SIZE
    import utils
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)


class Dot(pygame.sprite.Sprite) :
    """A memory dot on our grid display"""
    def __init__(self, x, y, num, clickable=False) :
        pygame.sprite.Sprite.__init__(self)
        if clickable :
            self.image, self.rect = utils.load_png("empty_circle.png")
        else :
            self.image, self.rect = utils.load_png("blue_circle.png")
        self.image = pygame.transform.scale(self.image, DOT_SIZE)
        self.rect = pygame.Rect(x, y, DOT_SIZE[0], DOT_SIZE[1])
        self.num = num
        self.clickable = clickable
        self.clicked = False

    def update(self) :
        """Calls the hide function once the user indicates that they have memorized the dots"""
        if self.clicked :
            self.image, _ = utils.load_png("empty_circle.png")
            self.image = pygame.transform.scale(self.image, DOT_SIZE)
            self.clicked=False
        else :
            self.image, _ = utils.load_png("white_circle.png")
            self.image = pygame.transform.scale(self.image, DOT_SIZE)
            self.clicked=True
    
    