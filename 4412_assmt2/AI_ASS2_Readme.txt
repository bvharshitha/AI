

##Programming Language
Language: Python
Version: Python 3.8.10


##Code Structure
The code is organized into the following components:

1.GameState Class: Manages the current game state, including the number of red and blue marbles, checking for game over conditions, calculating scores, and determining possible moves.

2.Minimax Algorithm with Alpha-Beta Pruning: Implements the decision-making logic for the AI player, optimizing the search for the best move by using alpha-beta pruning to reduce the number of evaluated game states.

3.Evaluation Function: The evaluation function assesses the game's current state by assigning a score based on the remaining marbles (2 points per red and 3 per blue) and the number of possible moves. For ongoing games, it values states with more marbles and more move options. In standard mode, higher scores are preferred, while in misère mode, lower scores are better, helping the AI make decisions that align with the winning strategy for each mode.

4.Human Move Input Handling: Manages user input for human players, ensuring that inputs are valid and within the game’s rules.

5.Main Game Loop: Controls the flow of the game, alternating turns between the computer and human players, and checking for game-ending conditions.


##How to Run the Code

python red_blue_nim.py <num-red> <num-blue> <Version> <first-player> <depth>

Version: standard or misere
first-player: computer or human
num-blue,num-red: can be changed to required count

eg: python red_blue_nim.py 5 5 standard computer 10 
