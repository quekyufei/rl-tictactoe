import pickle

from numpy.random import choice as random_choice

from .player import Player

class SimpleRlBot(Player):
	'''
	Implementation of tic-tac-toe bot as described in the introduction of Stutton's book.

	Simple RL player that stores a value for each state that it has seem before.
	At each turn, it looks through all legal states and their associated values.
	Uses epsilon-greedy to chose action to take.
	
	Throughout a game, it will store a history of moves that it made
	Value of each state visited is updated using the TD update rule: V(S) = V(S) + alpha * [V(S+1) - V(S)]
	Exploratory moves do not update the values.
	'''


	def __init__(self, mark, learning_rate, pickle_file):

		Player.__init__(self, mark)
		self.last_move = None
		self.learning_rate = learning_rate
		self.pickle_file = pickle_file
		# TODO perhaps decaying epsilon?
		self.epsilon = 0.05

		with open(self.pickle_file, 'rb') as f:
			self.state_dict = pickle.load(f)

	def get_move(self, board):
		legal_moves = board.get_legal_moves(self.mark)

		do_explore = random_choice([True,False], 1, p=[self.epsilon, 1 - self.epsilon])

		if do_explore:
			# epsilon greedy method. Choosing random exploratory move
			choice = random_choice(legal_moves)
			choice = self.get_value(choice)
			if self.last_move:
				self.last_move.set_exploratory(True)

		else:
			# get list of all states with the highest value 
			best_states = self.get_best_states(legal_moves)

			# randomly choose a state if there are ties in value
			choice = random_choice(best_states)

		# set up link to previous move
		choice.set_previous_move(self.last_move)
		self.last_move = choice

		# returns chosen move
		return choice

	def get_best_states(self, legal_moves):
		'''
		Input: legal moves - list of Move objects corresponding to legal future states

		Fetches the scores for each state.
		Keeps a list that consist of Moves that have the highest score.
		If a Move has higher score than the existing ones, replace the list with this new Move

		Returns a list of moves, all of which have the same score.
		'''
		best_moves_list = []

		for move in legal_moves:
			move = self.get_value(move)
			
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

	def get_value(self, move):
		# retrieve score from dictionary; if entry does not exist, initialise with value of 0.5
		if move.state in self.state_dict:
				move.value = self.state_dict[move.state]
		else:
			self.state_dict[move.state] = 0.5
			move.value = 0.5

		return move

	def game_ended(self, result):

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