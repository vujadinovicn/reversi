# Reversi/Othello game

This repository represents Reversi/Othello game made as a project for course of _Algorithms and data structures_.

### Reversi
Reversi is a strategy board game for two players, played on an 8×8 board. More informations on this game be found using link https://en.wikipedia.org/wiki/Reversi.

Reversi was chosen as an idea for project which will include data structures - tree and maps as well as Minimax algorithm for allowing the user to play against AI.

### Application flow
Project is made as an console application. 
Boards field can be empty - not yet obtained by any player and can not be obtained in current play or it can contain one of the next three letters:
- B - human's  disk (black)
- W - AI's disk (white)
- O - represents field where user (human) can place B disk in current round

When the application is started console will show the board and offer human to select the field to place disk.  
Human has to type column letter and row number. If the field is not properly selected (field not labelled with O), error messages will show.  
After the human has placed its disk, console will show state after its move. Immediately after this, AI will play its turn and console will show state after its move.   
Now, human can place its disk again. This algorithm repeats until the very end.  
When there are no moves left for one of the players (or both), game will end and console with print out the winner of the game. 
 
Here is how it looks  
![cetvrta](https://user-images.githubusercontent.com/96585470/224315235-193ff5c7-1720-47ac-8974-67d1d655b4de.png)



### AI in project
In this project, game has been made to be played between human and computer (AI). 
Main algorithm for AI is Minimax algorithm. It also includes alpha and beta pruning. 
Heuristics has been made by going over some details and tactics in Reversi game mainly by using internet.  
Python file which includes all of this is ``game.py``.

### Optimization
Games board is represented as an binary number (for black board it's ``0b0000000000000000000000000000100000010000000000000000000000000000``). Also, first and last column, as well as first and last row are represented through binary numbers. This is used for setting new disk on board the faster way. Methods for setting new disk on board, getting field information, calculating current score and heuristic score i.e. everything including board fields and operations on them are using bitwise operations with binary numbers other than using arrays.

### Project structure
Project is divided into folders/packages with ``main.py`` module for running the application.

##### games package
Most important package containing:
- ``constants.py`` - contains binary number constants for moving up, down, left, right and black and white board represented as binary numbers
- ``game.py`` - most important script containing ``Game`` class which contains methods for moving across the board, AI play, human play, calculating heuristic and other helper methods
##### game_table package
Contains two modules
- ``board.py`` - contains class ``Board`` with attributes of black and white state. Main purpose is drawing the board
- ``state.py`` - contains class ``State`` with methods for getting and setting board fields and calculating current score.
##### maps package 
Contains ``hash_map.py``, ``map.py``, ``map_element.py`` for managing map data structure.
##### trees package 
Contains ``tree.py`` and ``tree_node.py`` for managing tree data structure.

### Imports and running the application
There is no need to install any external libraries in this project.
When the virtual environment is created and activated, application can be ran from ``main.py``. 

### Endnotes
This project was made in my first year of faculty during summer semestar. At that time I haven't been using git and GitHub and that is the reason why this first and one commit consists the whole project. I tried to refactor it a bit so the arhitecture is better.
I'm currently learning AI in my third year and will aim to get some new knowledge of topics included in this project so it can be improved and better.
