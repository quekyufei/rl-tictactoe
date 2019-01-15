winning_combinations = [
	[0,1,2], [3,4,5], [6,7,8], # horizontals
	[0,3,6], [1,4,7], [2,5,8], # verticals
	[0,4,8], [2,4,6]
]


def main():
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
		if board[item[0]] == board[item[1]] == board[item[2]] and board[item[0]] != "-":
			return True
	return False


def print_board(board):
	print(board[0] + ' | ' + board[1] + ' | ' + board[2] + '\n')
	print(board[3] + ' | ' + board[4] + ' | ' + board[5] + '\n')
	print(board[6] + ' | ' + board[7] + ' | ' + board[8] + '\n')


if __name__ == '__main__':
	main()