

try:
    import sys
    import pygame
    import utils
    import instruction_page
    import survey_page
    import grid
    import global_vars
    import time
    import csv
    import numpy as np
    import sounddevice as sd
    from socket import *
    from pygame.locals import *
    import os
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)

# BEEP is commented out for now because it isn't working on my mac! TODO troubleshoot
# TODO Make sure csv writes to the Memory-Interface directory, not the terminal's directory (CWD)
def beep(frequency=19000, duration=0.3, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    sd.play(wave, sample_rate)
    sd.wait()

def save_timestamps(participant_num, timestamps):
    with open(f'timestamps_{participant_num}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Stage', 'Absolute Timestamp (s)', 'Stage Duration (s)'])
        prev_time = 0
        for stage, ts in timestamps.items():
            duration = ts - prev_time
            writer.writerow([stage, f"{ts:.4f}", f"{duration:.4f}"])
            prev_time = ts

def main():
    # First enter participant information in terminal
    user_exists = True
    print(global_vars.INITIAL_TEXT)
    while user_exists :
        participant_num = input("\nPlease enter participant number or command: ")
        if participant_num.strip() == "help" :
            print(global_vars.HELP)
        elif participant_num.strip() == "quit" :
            return
        elif participant_num.strip() == "show" :
            utils.print_user_list()
        else :
            user_exists = utils.does_user_exist(participant_num)
            if user_exists :
                print(global_vars.USER_EXISTS)
    print("\n\n\n\n\n")

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode(global_vars.SCREEN_SIZE)
    pygame.display.set_caption('Memory Game')

    # Load map images
    map_images = []
    fpath = os.path.dirname(os.path.realpath(__file__))
    for i in range(global_vars.NUM_ROUNDS):
        img = pygame.image.load(f"{fpath}/maps/map{i+1}.jpg").convert()
        img = pygame.transform.scale(img, global_vars.SCREEN_SIZE)
        map_images.append(img)

    # Initialize instruction pages
    instructions_0 = instruction_page.Instructions(global_vars.SCREEN_SIZE, global_vars.INSTRUCTIONS_0)
    instructions_1 = instruction_page.Instructions(global_vars.SCREEN_SIZE, global_vars.INSTRUCTIONS_1)
    instructions_2 = instruction_page.Instructions(global_vars.SCREEN_SIZE, global_vars.INSTRUCTIONS_2)
    instructions_4 = instruction_page.Instructions(global_vars.SCREEN_SIZE, global_vars.INSTRUCTIONS_4)
    instructions_5 = instruction_page.Instructions(global_vars.SCREEN_SIZE, global_vars.INSTRUCTIONS_5)

    # Initialize game itself
    mem_display_background = pygame.Surface(global_vars.SCREEN_SIZE)
    mem_display_background.convert()
    mem_display_background.fill(global_vars.BACKGROUND_COLOR)
    mem_grid = grid.Grid(mem_display_background)

    click_mem_background = pygame.Surface(global_vars.SCREEN_SIZE)
    click_mem_background.convert()
    click_mem_background.fill(global_vars.BACKGROUND_COLOR)
    click_grid = grid.Grid(click_mem_background, dot_locs=mem_grid.dot_locs)

    survey_pg = survey_page.SurveyPage(global_vars.SCREEN_SIZE, 5, ["1","2","3","4","5"], "round confidences", global_vars.QUESTION_2)
    survey_pg_2 = survey_page.SurveyPage(global_vars.SCREEN_SIZE, 2, ["Y","N"], "2048 prediction", global_vars.QUESTION_1)

    screen.blit(instructions_0, (0, 0))
    pygame.display.flip()

    instructions_state = 0
    past_instructions = False
    page_num = 0

    clock = pygame.time.Clock()
    timer_started = False
    total_time = 3000
    can_time = True

    timestamps = {}
    experiment_start_time = time.time()

    while True:
        if (past_instructions and page_num % global_vars.NUM_PAGES == 0) and can_time:
            if not timer_started :
                clock.tick(60)
                timer_started = True
            else :
                total_time -= clock.tick(60)
            if total_time <= 0 :
                page_num += 1
                screen.blit(map_images[page_num // global_vars.NUM_PAGES], (0, 0))
                timer_started = False
                total_time = 3000

        for event in pygame.event.get():
            if event.type == QUIT:
                save_timestamps(participant_num, timestamps)
                return
            if past_instructions:
                if page_num >= global_vars.NUM_PAGES * global_vars.NUM_ROUNDS - 1:
                    screen.blit(instructions_5, (0,0))
                    click_grid.write_score(participant_num)
                    survey_pg.write(participant_num)
                    survey_pg_2.write(participant_num)
                    can_time = False
                # Just as a note, if the event is not KEYDOWN then it won't have a key field
                # I think this works because python returns none for nonexistent fields
                # So you probably only need the second part of the condition anyways
                elif page_num % global_vars.NUM_PAGES == 0 :
                    screen.blit(mem_display_background, (0, 0))
                    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                        page_num += 1
                        now = time.time()
                        timestamps[f"dots_display_round_{page_num}"] = now - experiment_start_time
                        # beep()
                elif page_num % global_vars.NUM_PAGES == 1 :
                    current_round = page_num // global_vars.NUM_PAGES
                    screen.blit(map_images[current_round], (0, 0))
                    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                        page_num += 1
                        now = time.time()
                        timestamps[f"map_display_round_{page_num}"] = now - experiment_start_time
                        # beep()
                elif page_num % global_vars.NUM_PAGES == 2 :
                    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                        page_num += 1
                        click_grid.tally()
                        now = time.time()
                        timestamps[f"dots_recall_round_{page_num}"] = now - experiment_start_time
                        # beep()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        click_grid.update_dots(mouse_pos)
                    screen.blit(click_mem_background, (0,0))
                elif page_num % global_vars.NUM_PAGES == 3 :
                    screen.blit(survey_pg, (0,0))
                    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                        survey_pg.save()
                        screen.blit(survey_pg, (0,0)) # TODO figure out how to reset button clicked!
                        page_num += 1
                        screen.blit(survey_pg_2, (0,0))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        survey_pg.update(mouse_pos)
                        survey_pg.draw()
                elif page_num % global_vars.NUM_PAGES == 4 :
                    screen.blit(survey_pg_2, (0,0))
                    if event.type == pygame.KEYDOWN and event.key == K_RETURN:
                        survey_pg_2.save()
                        screen.blit(survey_pg_2, (0,0)) # Reset selected
                        page_num += 1
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        survey_pg_2.update(mouse_pos)
                        survey_pg_2.draw()
                else :
                    screen.blit(instructions_4, (0,0))
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_RETURN:
                            page_num += 1
                            screen.blit(survey_pg_2, (0,0))
                            mem_grid.arrange_dots()
                            click_grid.arrange_dots(mem_grid.dot_locs)
                            screen.blit(mem_display_background, (0, 0))
            elif event.type == pygame.MOUSEBUTTONDOWN :
                if instructions_state == 0:
                    instructions_state = 1
                    screen.blit(instructions_1, (0, 0))
            elif event.type == pygame.KEYDOWN:
                if instructions_state == 2:
                    if event.key == K_RETURN:
                        past_instructions = True
                if not past_instructions:
                    if event.key == K_RIGHT:
                        if instructions_state == 1:
                            instructions_state = 2
                    elif event.key == K_LEFT: 
                        if instructions_state == 2:
                            instructions_state = 1
                    if instructions_state == 1:
                        screen.blit(instructions_1, (0, 0))
                    elif instructions_state == 2:
                        screen.blit(instructions_2, (0, 0))

        pygame.display.flip()

if __name__ == '__main__': main()
