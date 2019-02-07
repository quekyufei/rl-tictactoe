import pickle
import random

from .player import Player

class SimpleRlBot(Player):
	'''
	Simple RL player that stores a value for each state that it has seem before.
	At each turn, it looks through all legal states and their associated values.
	Greedily chooses action to take.
	
	Throughout a game, it will store a history of states that it saw
	Depending on the result, it will increment or decrement the value in it's dictionary for the states seen.
	The increase/decrease is determined by the learning rate, and the multiplier for the results
	'''


	def __init__(self, mark, learning_rate, pickle_file):

		Player.__init__(self, mark)
		self.last_move = None
		self.learning_rate = learning_rate
		self.pickle_file = pickle_file

		with open(self.pickle_file, 'rb') as f:
			self.state_dict = pickle.load(f)

	def get_move(self, board):
		legal_moves = board.get_legal_moves(self.mark)

		# get list of all states with the highest value 
		best_states = self.get_best_states(legal_moves)

		# randomly choose a state if there are ties in value
		choice = random.choice(best_states)

		# set up link to previous move
		choice.set_previous_move(self.last_move)
		self.last_move = choice

		# TODO test and remove
		# self.move_history.append(self.move_and_get_string(board.board, choice))

		# returns chosen move
		return choice

	def get_best_states(self, legal_moves):
		'''
		Input: states - list of possible states after bot makes a legal move

		Fetches the scores for each state.
		Keeps a list that consist of states that have the highest score.
		If a state has higher score than the existing ones, replace the list with this new state

		Returns a list of (state, value) tuples, all of which have the same score.
		'''
		best_moves_list = []

		for move in legal_moves:
			# retrieve score from dictionary; if entry does not exist, initialise with value of 0.5
			state = move.state
			if state in self.state_dict:
				move.value = self.state_dict[state]
			else:
				self.state_dict[state] = 0.5
				move.value = 0.5

			if len(best_moves_list) == 0:
				best_moves_list.append(move)
			else:
				# if the current state's score is more than the score of the Moves in the list
				if move.value > best_moves_list[0].value:
					best_moves_list = [move]
				# if it is the same, add on to the list
				elif move.value == best_moves_list[0].value:
					best_moves_list.append(move)
				# else do nothing

		return best_moves_list

	# TODO test and remove
	# def move_and_get_string(self, board, move):
	# 	tmp = list(board)
	# 	tmp[move] = self.mark
	# 	return str(tmp)

	def game_ended(self, result):
		'''
		Update weights for each state
		Currently simply adds / subtracts the learning rate value to / from all moves that led to the win / loss.
		'''
		Player.game_ended(self, result)

		if result == 'win':
			end_value = 1
		elif result == 'loss':
			end_value = 0
		else:
			end_value = 0.5

		self.last_move.update_values(end_value, self.learning_rate, self.state_dict)

		self.last_move = None

	def all_done(self):
		self.save_dictionary()

	def save_dictionary(self):
		with open(self.pickle_file,'wb') as f:
			pickle.dump(self.state_dict, f)