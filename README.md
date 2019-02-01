# rl-tictactoe

RL trained bots to play the simple game of tic-tac-toe

### Current progress

- X and O player are separately trained with different "Q-tables".
- Pseudo "Q Tables" store states that are seen by the bots, and a value assigned to each of these states.
- Greedy actions are chosen during training

### Issues to address

- Greedy actions might be causing some issues due to the lack of exploration: consecutive games could be played identically.
- Currently scores are increased by a flat learning rate; this might have some drawbacks in that even if a new move was discovered that had a positive impact, it will have a far lower score compared to moves that have been seen many times before. Consider using another scoring system, perhaps percentage win?
- Even after a few thousand games played, bots do not seem "intelligent" as they still sometimes fail to block simple wins.
- I would expect the number of ties to increase as the bots get trained (it is always possible to draw in tictactoe) but so far this behaviour has not been displayed.
- The relative multipliers given to the results of win, loss, and ties play a big role.
