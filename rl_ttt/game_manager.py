winning_combinations = [
	[0,1,2], [3,4,5], [6,7,8], # horizontals
	[0,3,6], [1,4,7], [2,5,8], # verticals
	[0,4,8], [2,4,6]					 # diagonals
]

class Board():
	def __init__(self, verbose=False):
		self.verbose = verbose

	def has_winner(self):
		# check if any player has won the game
		for item in winning_combinations:
			if self.board[item[0]] == self.board[item[1]] == self.board[item[2]] and self.board[item[0]] != '-':
				return True

	def has_draw(self):
		if not any([True for i in self.board if i == '-']):
			return True
		else:
			return False

	def get_legal_moves(self, mark):
		list_positions = [ i for i in range(9) if self.board[i] == '-' ]
		moves_list = []
		for position in list_positions:
			# create Move object and append it to list
			moves_list.append( Move(list(self.board), position, mark) )

		return moves_list

	def make_move(self, move, mark):
		# replace '-' with player's symbol
		self.board[move] = mark
		if self.verbose:
			self.print()

	def is_move_legal(self, move):
		# move should be an integer from 0 - 8, corresponding to the position on the board
		if self.board[move] != '-':
			return False
		else:
			return True

	def print(self):
		print(self.board[0] + ' | ' + self.board[1] + ' | ' + self.board[2] + '\n')
		print(self.board[3] + ' | ' + self.board[4] + ' | ' + self.board[5] + '\n')
		print(self.board[6] + ' | ' + self.board[7] + ' | ' + self.board[8] + '\n')	


	def initialise_board(self):
		self.board = ['-']*9
		if self.verbose:
			self.print()

class Move():
	def __init__(self, board, position, mark):
		board[position] = mark
		self.state = str(board)
		self.exploratory = False
		self.previous_move = None
		self.value = None

	def update_values(self, next_move_value, alpha):
		# TD learning value update
		self.value = self.value + alpha * (next_move_value - self.value)
		# recursively updates value of every move
		self.previous_move.update_values(self.value, alpha)

	def set_previous_move(self, move):
		self.previous_move = move

	def set_exploratory(self, boolean):
		self.exploratory = boolean