try:
    import sys
    import os
    import pygame
    import json
    import utils
    import dot
    from socket import *
    from pygame.locals import *
    from global_vars import DOT_SIZE, SPACER, START_X, START_Y, STORAGE_PATH, BACKGROUND_COLOR
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)

class Grid(pygame.sprite.Sprite) :
    """A grid which contains dots and their locations"""
    def __init__(self, background: pygame.Surface, dot_locs=None) :
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_png("grid.png")
        grid_size = (DOT_SIZE[0]*5, DOT_SIZE[1]*5)
        self.image = pygame.transform.scale(self.image, grid_size)
        self.rect = pygame.Rect(0, 0, grid_size[0], grid_size[1])
        self.rect.center = (background.get_width()//2, background.get_height()//2)
        background.blit(self.image, self.rect)
        self.background = background
        self.dot_locs = None
        self.dot_list = None
        self.arrange_dots(dot_locs)
        self.score_hist = []
    
    def arrange_dots(self, dot_locs: list = None) :
        """Blits four dots to the grid in a random arrangement (for the initial grid)"""
        if self.dot_list != None :
            for dot_obj in self.dot_list :
                pygame.draw.rect(self.background, BACKGROUND_COLOR, dot_obj.rect)
        if dot_locs == None :
            locs = utils.rng(16,5)
            dot_list : list[dot.Dot] = []
            for i in locs :
                x_offset = START_X + SPACER * (i//4)
                y_offset = START_Y + SPACER * (i%4)
                rand_dot = dot.Dot(x_offset,y_offset,i)
                dot_list.append(rand_dot)
            for dot_obj in dot_list :
                self.background.blit(dot_obj.image, dot_obj.rect)
            self.dot_locs = locs
            self.dot_list = dot_list
        else :
            self.dot_locs = dot_locs
            self.dot_list = self.set_all_dots()
        

    def set_all_dots(self) :
        """For the click grid, we put clickable dots in each square for the user to 
        enter where they think the dots were placed earlier"""
        dot_list = []
        for i in range(0,16) :
            x_offset = START_X + SPACER * (i//4)
            y_offset = START_Y + SPACER * (i%4)
            click_dot = dot.Dot(x_offset,y_offset,i, True)
            dot_list.append(click_dot)
        for dot_obj in dot_list :
            self.background.blit(dot_obj.image, dot_obj.rect)
        return dot_list
    
    def update_dots(self, mousePos: tuple) :
        """Flips a dot's color if it was clicked on"""
        for dot_obj in self.dot_list:
            if dot_obj.rect.collidepoint(mousePos):
                dot_obj.update()
                pygame.draw.rect(self.background, BACKGROUND_COLOR, dot_obj.rect)
                self.background.blit(dot_obj.image, dot_obj.rect)
    
    def tally(self) :
        """Computes the score for a round and adds it to the grid's history"""
        score_dict = {
            "correct_dots" : self.dot_locs
        }
        clicked_dots = []
        score = 0
        for dot in self.dot_list :
            if dot.clicked :
                clicked_dots.append(dot.num)
                if dot.num in self.dot_locs :
                    score += 1
                else :
                    # we don't want people to be rewarded for selecting a bunch of wrong dots
                    score -= 1
        score_dict.update({
            "clicked_dots" : clicked_dots,
            "score" : score
            })
        self.score_hist.append(score_dict)

    
    def write_score(self, user: str) :
        """Writes data on the game outcome to a json file.
        Specifically, we write the user, the dots that were displayed, the dots that the 
        user picked, and the score.
        Score is defined as +1 for every correct dot selected and -1 for every incorrect
        dot selected, since we don't restrict how many dots a user can select"""
        if not os.path.exists(STORAGE_PATH) :
            with open(STORAGE_PATH, "w") as player_data :
                empty_dict = {}
                json.dump(empty_dict, player_data)
        json_data = {}
        with open(STORAGE_PATH, "r") as player_data :
            json_data = json.load(player_data)
            json_data.update({user : {"scores" : self.score_hist}})
        with open(STORAGE_PATH, "w") as player_data :
            json.dump(json_data, player_data, indent=2)
