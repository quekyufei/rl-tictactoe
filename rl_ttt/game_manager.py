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

	def get_legal_moves(self):
		return [ i for i in range(9) if self.board[i] == '-' ]

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