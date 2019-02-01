import sys

from rl_bot_v1 import *

winning_combinations = [
	[0,1,2], [3,4,5], [6,7,8], # horizontals
	[0,3,6], [1,4,7], [2,5,8], # verticals
	[0,4,8], [2,4,6]					 # diagonals
]

def main(argv):
	o_bot = rl_bot('O', 0.001, 'O_player.pickle')
	x_bot = rl_bot('X', 0.001, 'X_player.pickle')

	iterations = int(argv[0])
	num_ties = 0
	num_wins = 0
	for i in range(iterations):
		board = initialise_board()

		turn = 0
		player = o_bot
		tie = False

		# main loop
		while not has_game_ended(board):
			player = o_bot if (turn%2 == 0) else x_bot

			board1 = player.get_move(board)
			if board1 == board:
				# means that there is a tie
				tie = True
				break
			else:
				board = board1

			turn += 1
			# print_board(board)


		# exited loop
		print_board(board)

		if tie:
			print('Game ' + str(i+1) + ' tied!')
			o_bot.game_ended('tie')
			x_bot.game_ended('tie')
			num_ties += 1

		else:
			num_wins += 1
			print('Game ' + str(i+1) + ' Over! Winner is: ' + player.mark)
			if player==o_bot:
				o_bot.game_ended('win')
				x_bot.game_ended('loss')
			else:
				x_bot.game_ended('win')
				o_bot.game_ended('loss')

	o_bot.save_dictionary()
	x_bot.save_dictionary()
	print(str(num_ties) + ' ties, ' + str(num_wins) + ' wins')
	print('all done!')


def pvc():
	'''
	player v computer; not implemented yet this is just code for pvp
	'''
	human_player = argv[1]

	board = initialise_board()
	turn = 0
	if human_player == 'O':
		player = rl_bot('X', 0.01, 'X_player.pickle')
	else:
		player = rl_bot('O', 0.01, 'O_player.pickle')

	print_board(board)

	# main loop
	while not has_game_ended(board):
		player = "O" if (turn%2 == 0) else "X"
		turn += 1

		# Get user input (integer from 0 - 8) 
		user_in = int(raw_input('enter move: '))

		# square is not blank
		if board[user_in] != '-':
			print('That is not a blank square!')
			continue
		# number is invalid
		elif user_in not in range(0,9):
			print('Enter a number between 0 and 8.')
			continue
		
		else:
			# replace '-' with player's symbol
			board.pop(user_in)
			board.insert(user_in, player)

		print_board(board)

	# exited loop
	print("Game Over! Winner is: " + player)

def pvp():
	board = initialise_board()
	turn = 0
	player = "O"
	print_board(board)

	# main loop
	while not has_game_ended(board):
		player = "O" if (turn%2 == 0) else "X"
		turn += 1

		# Get user input (integer from 0 - 8) 
		user_in = int(raw_input('enter move: '))

		# square is not blank
		if board[user_in] != '-':
			print('That is not a blank square!')
			continue
		# number is invalid
		elif user_in not in range(0,9):
			print('Enter a number between 0 and 8.')
			continue
		
		else:
			# replace '-' with player's symbol
			board.pop(user_in)
			board.insert(user_in, player)

		print_board(board)

	# exited loop
	print("Game Over! Winner is: " + player)

def initialise_board():
	return ['-']*9


def has_game_ended(board):
	# check if any player has won the game
	for item in winning_combinations:
		if board[item[0]] == board[item[1]] == board[item[2]] and board[item[0]] != '-':
			return True
	
	
	return False


def print_board(board):
	print(board[0] + ' | ' + board[1] + ' | ' + board[2] + '\n')
	print(board[3] + ' | ' + board[4] + ' | ' + board[5] + '\n')
	print(board[6] + ' | ' + board[7] + ' | ' + board[8] + '\n\n')


if __name__ == '__main__':
	main(sys.argv[1:])