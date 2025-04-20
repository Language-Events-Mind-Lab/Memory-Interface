try:
    import sys
    import os
    from socket import *
    from pygame.locals import *
except ImportError as err:
    print(f"couldn't load module. {err}")
    sys.exit(2)

# Game Specs
NUM_ROUNDS = 3
NUM_PAGES = 6
# Terminal Colors
TERMINAL_BLUE = "\033[94m"
TERMINAL_RED = "\u001b[31m"
TERMINAL_WARNING = '\033[93m'
TERMINAL_END = "\033[0m"

# Instruction Text
INITIAL_TEXT = TERMINAL_WARNING + """Enter \"help\" for instructions on operating this game, \"quit\" to quit, 
or \"show\" to display a list of users that have already gone""" + TERMINAL_END

HELP = TERMINAL_BLUE + """\n-----------------HELP------------------
After entering the participant number into the terminal, the game will launch.
\nThe participant will read the instructions and view the grid. Ensure that before the experiment,
the participant has switched to the screen directly after the display grid, which should say, 
\"At the end of the experiment, press ENTER again on this window.\"
\nIf there are any issues before this point, please quit the game and start again.
\nAfter the experiment, they will be prompted to click on the dots on the grid that correspond
to those displayed earlier. \n\nWhen they are done, they MUST press enter and then close the window
to save their responses.
\n-----------------HELP------------------""" + TERMINAL_END

USER_EXISTS = TERMINAL_RED + """\n\nThis participant number has been used.
\nIf this participant number hasn't gone yet, please press Ctrl-C or enter "quit" to quit the program.
\nYou may need to check the data file for any anomalies.""" + TERMINAL_END
INSTRUCTIONS_0 = ["", """CLICK on this page to start!"""]
INSTRUCTIONS_1 = ["""In this experiment, you are the SPEAKER, and your partner is the LISTENER.""",
                  "",
                  """You will be shown a series of maps and a simple memory game.""",
                  "",
                  """Your objective is to successfully complete both the MAP TASK and the MEMORY TASK""",
                  "",
                  """Press RIGHT ARROW to continue"""]
INSTRUCTIONS_2 = ["""In the MAP TASK, you will be conversing with your partner and giving them directions""",
                  """to a specified point on the map.""",
                  "",
                  """You are both given maps of the same locations, with some slight differences.""",
                  "",
                  """You will need to communicate with your partner to help them understand how to""",
                  """reach the destination point.""",
                  "",
                  """Press RIGHT ARROW to continue, or LEFT ARROW to go back"""]
INSTRUCTIONS_3 = ["""In addition to the MAP TASK, you will also be asked to perform a MEMORY TASK.""", 
                  "",
                  """At the beginning of each map trial, you will see 5 dots randomly arranged on a grid""",
                  """for THREE seconds, after which the map will be displayed.""",
                  "",
                  """Your job is to remember this configuration as best you can.""",
                  "",
                  """You will be asked to recreate this configuration at the end of each map trial.""",
                  "",
                  """Press RIGHT ARROW to continue, or LEFT ARROW to go back"""]
INSTRUCTIONS_6 = ["", """Press ENTER when ready to display the MEMORY TASK, or LEFT ARROW to go back"""]
INSTRUCTIONS_4 = ["""Your responses for this trial have been saved.""", 
                  """You may press ENTER to move to the next page."""]
INSTRUCTIONS_5 = ["""Thanks for your participation!""", 
                  """You may now close the window."""]
QUESTION_1 = ["""Do you think this was a 2048 trial?"""]
QUESTION_2 = ["""How confident are you in your response?"""]

STORAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "player_data.json")

# Dot Rendering
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
DOT_SIZE = (int((170/1200)*SCREEN_WIDTH), int((170/1200)*SCREEN_WIDTH))
SPACER = int((180.2/1200)*SCREEN_WIDTH)
START_X = (246.5/1200)*SCREEN_WIDTH
START_Y = SCREEN_HEIGHT//2-DOT_SIZE[1]*2.1

# Button Rendering
BUTTON_SIZE = int((55/1200)*SCREEN_WIDTH)
BUTTON_SPACING = int((80/1200)*SCREEN_WIDTH)
FONT_SIZE = int(0.03 * SCREEN_WIDTH)

# Text Rendering
UPPER_TEXT = int((200/800)*SCREEN_HEIGHT)

# Game Colors
FONT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (32, 81, 111)

