import random

class Player():
	def __init__(self, mark):
		self.mark = mark
		self.num_wins = 0
		self.num_losses = 0
		self.num_draws = 0

	def get_move(self, board):
		# returns integer corresponding to move
		pass

	def game_ended(self, result):
		if result == 'win':
			self.num_wins += 1
		elif result == 'loss':
			self.num_losses += 1
		else:
			self.num_draws += 1

	def all_done(self):
		pass

class HumanPlayer(Player):
	def __init__(self, mark):
		Player.__init__(self, mark)

	def get_move(self, board):
		while True:
			# Get user input (integer from 0 - 8) 
			user_in = int(input('Enter move: '))

			# number is invalid
			if user_in not in range(0,9):
				print('Enter a number between 0 and 8.')
				continue

			# square is not blank
			if board.is_move_legal(user_in):
				return board.get_move_object(user_in, self.mark)
			else:
				print('Move is not legal.')

class RandomPlayer(Player):
	def __init__(self, mark):
		Player.__init__(self, mark)

	def get_move(self, board):
		return random.choice(board.get_legal_moves(self.mark))