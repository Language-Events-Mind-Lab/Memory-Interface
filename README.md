## Setup
To get this game onto a computer, you must first be logged into github on the computer. 
You can refer to [this](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) guide for cloning a repository to your computer.
Additionally, you can install GitHub desktop on the computer, sign in, and clone the repository from there (which is less finicky).

To run this game, you will need the pygame library installed. To do so, navigate to the memory_game folder on your terminal and run the command `pip install -r requirements.txt`.
If pip is not installed on your computer, you will first need to install it [here](https://pip.pypa.io/en/stable/installation/).
Alternatively, you could just run `pip install pygame` but this is not recommended.

## Running the Game
The game can be run by typing the command `python3 main.py` into a terminal running from inside the game folder. 
If you're getting some sort of file not found issue (or you're running the program from outside the folder), find `main.py` in your file system, copy its absolute path and run the command `python3 [abs_path]`, replacing `[abs_path]` with the path you just copied.

The game will first prompt the experimenter to enter an ID for the participant (whether that's a number or a name doesn't really matter, but it must be unique).
If the ID has been used before, the game will prompt the experimenter again to enter the ID. 
If the ID shouldn't have been used before, the experimenter should type the command "show" into the command prompt see which users have gone already.

## Playing the Game
Once the user information has been entered, the game will appear as a pop-up window. The participant will be prompted to read the instructions and memorize the locations of five dots on a 4x4 grid.
There will be a pause screen after this, after which the participant will be asked to complete the actual experiment.

After the experiment, the participant will attempt to click the correct locations of the dots on the grid, and press ENTER to save their responses.
Ensure that the participant does NOT close the game before saving their responses; they will only save when the game is closed on the last screen, after the grid.

## Storing Data
Once the game is closed, data on the run will be saved to `player_data.json`, which will automatically be created in the game folder.
This file is keyed to participant ID (hence the restrictions on duplicates) and contains the list of correct dots, the list of dots entered by the user, and their "score"

Score is calculated as the number of correct dots selected minus the number of incorrect dots selected, so selecting three correct dots and one incorrect dot will yield a score of two, not three.
