## Setup
To get this game onto a computer, you must first be logged into github on the computer. 
You can refer to [this](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) guide for cloning a repository to your computer.
Additionally, you can install GitHub desktop on the computer, sign in, and clone the repository from there (which is less finicky).

To run this game, you will need the pygame library installed. To do so, navigate to the memory_game folder on your terminal and run the command `pip install -r requirements.txt`.
If pip is not installed on your computer, you will first need to install it [here](https://pip.pypa.io/en/stable/installation/).
Alternatively, you could just run `pip install pygame` but this is not recommended.

## Running the Game
You should run this game by opening VSCode (either by searching up VSCode on the bottom left search bar or by opening Github Desktop, navigating to the Memory-Interface repository, and pressing the option to open the repository in VSCode), clicking on `maincomb.py` in the sidebar, and pressing the play button. If you don't see files on the sidebar, you should make sure that the icon on the far left with two documents is selected:

![docicon](md_images/docicon.png)

In addition, the game can be run by typing the command `python3 maincomb.py` into a terminal running from inside the game folder. 
If you're getting some sort of file not found issue with the latter method (or you're running the program from outside the folder), find `maincomb.py` in your file system, copy its absolute path and run the command `python3 [abs_path]`, replacing `[abs_path]` with the path you just copied.

The game will first prompt the experimenter to enter an ID for the participant into the terminal (whether that's a number or a name doesn't really matter, but it must be unique).
If the ID has been used before, the game will prompt the experimenter again to enter the ID. 
If the ID shouldn't have been used before, the experimenter should type the command "show" into the command prompt see which users have gone already.

## Playing the Game
Once the user information has been entered, the game will appear as a pop-up window. The speaker will be prompted to read their instructions, after which a screen will prompt them to begin the experiment when ready. Upon beginning, they will be shown a grid for three seconds, after which their map for the round will display

After the map task, the participant will attempt to click the correct locations of the dots on the grid, and press ENTER to save their responses. They will then answer how confident they were in their responses and whether they thought this was a 2048 trial. They will start the next trial after this.

After six rounds, the experiment will be complete and the speaker will be able to close the window, upon which the responses will be saved. Ensure that the participant does NOT close the game before saving their responses; they will only save when the game is closed on the last screen, after the grid.

## Storing Data
Once the game is closed, data on the run will be saved to `player_data.json`, which will automatically be created in the game folder.
This file is keyed to participant ID (hence the restrictions on duplicates) and contains the list of correct dots, the list of dots entered by the user, and their "score". It also contains survey responses

Score is calculated as the number of correct dots selected minus the number of incorrect dots selected, so selecting three correct dots and one incorrect dot will yield a score of two, not three.

Separately, a list of timestamps will be stored at `timestamps_{participant number}.csv`. Each round will create a *separate* timestamp file, as opposed to `player_data.json`, which contains data for all participants.
