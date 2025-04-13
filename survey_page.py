try:
    import sys
    import pygame
    import utils
    import json
    from global_vars import *
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print(f"couldn't load module. {err}")
    print("with love, survey_page.py")
    sys.exit(2)

class SurveyPage(pygame.Surface) :
    """A page that asks questions after the trial"""
    def __init__(self, screen_size: tuple, num_buttons: int, button_text: list, name: str, question_text: str) :
        pygame.Surface.__init__(self, screen_size)
        self.convert()
        self.fill(BACKGROUND_COLOR)
        self.num_buttons = num_buttons
        self.button_text = button_text
        self.name = name

        self.font = pygame.font.Font(None, FONT_SIZE)
        self.buttons = []
        self.selected_button = None

        utils.render_text(question_text, self, screen_size[1]//4)

        left_button_pos = screen_size[0]//2 - ((self.num_buttons-1)/2)*(BUTTON_SIZE + BUTTON_SPACING)
        for i in range(self.num_buttons) :
            rect = pygame.Rect(left_button_pos + i * (BUTTON_SIZE + BUTTON_SPACING), screen_size[1]//2, BUTTON_SIZE, BUTTON_SIZE)
            self.buttons.append((rect, i+1))
        
        self.prev_selected = []
        self.draw()

    def draw(self) :
        """Renders the buttons"""
        for (i, (rect, num)) in enumerate(self.buttons) :
            color = (100, 100, 255) if self.selected_button == num else (200, 200, 200)
            pygame.draw.rect(self, color, rect)

            # Button number
            text = self.font.render(str(self.button_text[i]), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            self.blit(text, text_rect)

    def update(self, mousePos: tuple) :
        """Updates state based on selected button"""
        for rect, num in self.buttons:
            if rect.collidepoint(mousePos):
                self.selected_button = num

    def save(self) :
        """Saves the state history"""
        self.prev_selected.append(self.selected_button)
        self.selected_button = None

    def write(self, user: str) :
        """Writes state history to JSON; this must be run AFTER the grid write"""
        with open(STORAGE_PATH, "r") as player_data :
            json_data = json.load(player_data)
            json_data[user].update({self.name : self.prev_selected})
        with open(STORAGE_PATH, "w") as player_data :
            json.dump(json_data, player_data, indent=2)