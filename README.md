# rl-tictactoe

RL trained bots to play the simple game of tic-tac-toe.
Implementation of method described in Introduction of Stutton's book

### Details

- O and X player are separately trained with different value tables.
- Each state is initialised with a score of 0.5
- At every turn, players look up the value of all the possible legal states from the current position
- Actions are then chosen using the epsilon-greedy policy.
- At the end of each game, values of each state are updated, except for the states from which an exploratory move was chosen.
