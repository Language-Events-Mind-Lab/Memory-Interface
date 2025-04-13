try:
    import sys
    import pygame
    import utils
    import instruction_page
    import survey_page
    import grid
    import global_vars
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)

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

    # Initialize instruction pages
    instructions_0 = instruction_page.Instructions(global_vars.SCREEN_SIZE, global_vars.INSTRUCTIONS_0)
    instructions_1 = instruction_page.Instructions(global_vars.SCREEN_SIZE, global_vars.INSTRUCTIONS_1)
    instructions_2 = instruction_page.Instructions(global_vars.SCREEN_SIZE, global_vars.INSTRUCTIONS_2)
    instructions_3 = instruction_page.Instructions(global_vars.SCREEN_SIZE, global_vars.INSTRUCTIONS_3)
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
    
    # Blit initial instruction page to the screen
    screen.blit(instructions_0, (0, 0))
    pygame.display.flip()

    # Initialize page variable
    instructions_state = 0
    past_instructions = False
    page_num = 0

    # Initialize timer
    clock = pygame.time.Clock()
    timer_started = False
    total_time = 3000
    can_time = True
    
    # Event loop
    while True:
        if (past_instructions and page_num % global_vars.NUM_PAGES == 0) and can_time:
            if not timer_started :
                clock.tick(60)
                timer_started = True
            else :
                total_time -= clock.tick(60)
            if total_time <= 0 :
                page_num += 1
                screen.blit(instructions_3, (0, 0))
                timer_started = False
                total_time = 3000

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if past_instructions:
                if page_num >= global_vars.NUM_PAGES * global_vars.NUM_ROUNDS :
                    screen.blit(instructions_5, (0,0))
                    click_grid.write_score(participant_num)
                    survey_pg.write(participant_num)
                    survey_pg_2.write(participant_num)
                    can_time = False
                elif page_num % global_vars.NUM_PAGES == 0 :
                    screen.blit(mem_display_background, (0, 0))
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_RETURN:
                            page_num += 1
                elif page_num % global_vars.NUM_PAGES == 1 :
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_RETURN:
                            page_num += 1
                    screen.blit(instructions_3, (0, 0))
                elif page_num % global_vars.NUM_PAGES == 2 :
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_RETURN:
                            page_num += 1
                            click_grid.tally()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        click_grid.update_dots(mouse_pos)
                    screen.blit(click_mem_background, (0,0))
                elif page_num % global_vars.NUM_PAGES == 3 :
                    screen.blit(survey_pg, (0,0))
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_RETURN:
                            survey_pg.save()
                            screen.blit(survey_pg, (0,0)) # Reset selected
                            page_num += 1
                            screen.blit(survey_pg_2, (0,0))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        survey_pg.update(mouse_pos)
                        survey_pg.draw()
                else :
                    screen.blit(survey_pg_2, (0,0))
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_RETURN:
                            survey_pg_2.save()
                            screen.blit(survey_pg_2, (0,0)) # Reset selected
                            page_num += 1
                            mem_grid.arrange_dots()
                            click_grid.arrange_dots(mem_grid.dot_locs)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        survey_pg_2.update(mouse_pos)
                        survey_pg_2.draw()

            # The following is code for the instructions
            # It is confusing b/c you need to be able to switch forward/backward
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