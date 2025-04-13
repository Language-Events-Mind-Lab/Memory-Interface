try:
    import sys
    import random
    import os
    import pygame
    import json
    from global_vars import FONT_COLOR, STORAGE_PATH, FONT_SIZE
    from socket import *
    from pygame.locals import *
    import random
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)

def load_png(name: str):
    """ Load image and return image object"""
    fullname = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
            image.set_colorkey((0,0,0))
    except FileNotFoundError:
        print(f"Cannot load image: {fullname}")
        raise SystemExit
    return image, image.get_rect()

def render_text(text_lst:list, background: pygame.Surface, top: int) :
    """Simple fn for rendering instruction text"""
    font = pygame.font.Font(None, FONT_SIZE)
    for line, instruction_text in enumerate(text_lst) :
        text = font.render(instruction_text, 1, FONT_COLOR)
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        line_spacing = int((textpos.bottom-textpos.top) * 2.2)
        textpos.top = top + line * line_spacing
        textpos.bottom = top + line * line_spacing
        background.blit(text, textpos)

def rng(range_len: int, num_samples: int) :
    """Randomly generates the specified number of dot indices in the specified range 
    in a way that creates arrangements that are more difficult to memorize"""
    range_list=list(range(range_len))
    sample = []
    fixed_range=num_samples//2
    for i in range(0,fixed_range) :
        rand_idx = random.randint(0,len(range_list)-1)
        rand_num = range_list[rand_idx]
        sample.append(rand_num)
        new_range_list = []
        for nums_left in range_list :
            if nums_left//4 != rand_num//4 and nums_left%4 != rand_num%4 :
                new_range_list.append(nums_left)
            range_list = new_range_list
    for item in random.sample(range_list,num_samples-fixed_range) :
        sample.append(item)
    return sample
        
def does_user_exist(participant_num) :
    if not os.path.exists(STORAGE_PATH) :
        return False
    json_data = {}
    with open(STORAGE_PATH, "r") as player_data :
        json_data = json.load(player_data)
    return participant_num in json_data

def print_user_list() :
    if not os.path.exists(STORAGE_PATH) :
        print("No users have gone")
        return
    with open(STORAGE_PATH, "r") as player_data :
        json_data = json.load(player_data)
    for participant_num in json_data :
        print(participant_num)
