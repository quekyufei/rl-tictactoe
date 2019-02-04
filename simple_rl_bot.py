import pickle
import random

from player import Player

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
		self.move_history = []
		self.learning_rate = learning_rate
		self.pickle_file = pickle_file

		with open(self.pickle_file, 'rb') as f:
			self.state_dict = pickle.load(f)

	def get_move(self, board):
		legal_moves = board.get_legal_moves()

		# get list of all states with the highest value 
		best_states = self.get_best_states(legal_moves, board)

		# randomly choose a state if there are ties in value
		choice = random.choice(best_states)[0]
		
		self.move_history.append(self.move_and_get_string(board.board, choice))

		# returns chosen move
		return choice

	def get_best_states(self, moves, board):
		'''
		Input: states - list of possible states after bot makes a legal move

		Fetches the scores for each state.
		Keeps a list that consist of states that have the highest score.
		If a state has higher score than the existing ones, replace the list with this new state

		Returns a list of (state, value) tuples, all of which have the same score.
		'''
		score_list = []

		for move in moves:
			# retrieve score from dictionary; if entry does not exist, initialise with value of 0.5
			state = self.move_and_get_string(board.board, move)
			if state in self.state_dict:
				score = self.state_dict[state]
			else:
				self.state_dict[state] = 0.5
				score = 0.5

			if len(score_list) == 0:
				score_list.append((move, score))
			else:
				# if the current state's score is more than the score of the elements in the list
				if score > score_list[0][1]:
					score_list = [(move, score)]
				# if it is the same, add on to the list
				elif score == score_list[0][1]:
					score_list.append((move,score))

		return score_list

	def move_and_get_string(self, board, move):
		tmp = list(board)
		tmp[move] = self.mark
		return str(tmp)

	def game_ended(self, result):
		'''
		Update weights for each state
		Currently simply adds / subtracts the learning rate value to / from all moves that led to the win / loss.
		'''
		Player.game_ended(self, result)

		if result == 'win':
			multiplier = 1
		elif result == 'loss':
			multiplier = -1
		else:
			multiplier = -0.1

		for move in self.move_history:
			self.state_dict[move] += multiplier * self.learning_rate

		self.move_history = []

	def all_done(self):
		self.save_dictionary()

	def save_dictionary(self):
		with open(self.pickle_file,'wb') as f:
			pickle.dump(self.state_dict, f)