import pickle
import random

class rl_bot():
	# create new states based on the possible moves (all the "-")
	# idea: upon seeing new state, asmultiplier it value of 0.5
	# think about how to update the value after game ends

	def __init__(self, mark, learning_rate, pickle_file):

		self.mark = mark
		self.move_history = []
		self.learning_rate = learning_rate
		self.pickle_file = pickle_file

		with open(self.pickle_file, 'rb') as f:
			self.state_dict = pickle.load(f)

	def get_move(self, board):
		board_string = ''.join(board)

		# get possible next states
		legal_states = self.get_legal_states(board_string)
		# get list of all states with the highest value 
		best_states = self.get_best_states(legal_states)

		if len(best_states) == 0:
			return board

		# randomly choose a state if there are ties in value
		choice = random.choice(best_states)[0]
		
		self.move_history.append(choice)

		# returns state after chosen move. converts to list of characters
		return list(choice)

	def get_legal_states(self, board):
		# Looks for all blank tiles in board.
		# For each blank tile, replaces the '-' with player's mark
		# Returns list consisting of the new board states (each as a string) after making a move.
		state_list = []
		for i in range(len(board)):
			if board[i] == '-':
				tmp = board[:i] + self.mark + board[i+1:]
				state_list.append(tmp)

		return state_list

	def get_best_states(self, states):
		'''
		Input: states - list of possible states after bot makes a legal move

		Fetches the scores for each state.
		Keeps a list that consist of states that have the highest score.
		If a state has higher score than the existing ones, replace the list with this new state

		Returns a list of (state, value) tuples, all of which have the same score.
		'''
		score_list = []

		for state in states:
			# retrieve score from dictionary; if entry does not exist, initialise with value of 0.5
			if state in self.state_dict:
				score = self.state_dict[state]
			else:
				self.state_dict[state] = 0.5
				score = 0.5

			if len(score_list) == 0:
				score_list.append((state, score))
			else:
				# if the current state's score is more than the score of the elements in the list
				if score > score_list[0][1]:
					score_list = [(state, score)]
				# if it is the same, add on to the list
				elif score == score_list[0][1]:
					score_list.append((state,score))

		return score_list

	def game_ended(self, result):
		'''
		Update weights for each state
		Currently simply adds / subtracts the learning rate value to / from all moves that led to the win / loss.
		'''
		if result == 'win':
			multiplier = 1
		elif result == 'loss':
			multiplier = -1
		else:
			multiplier = -0.1

		for move in self.move_history:
			self.state_dict[move] += multiplier * self.learning_rate

		self.move_history = []

	def save_dictionary(self):
		with open(self.pickle_file,'wb') as f:
			pickle.dump(self.state_dict, f)