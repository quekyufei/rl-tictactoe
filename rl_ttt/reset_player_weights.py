import pickle

state_dict = {}

with open('O_player.pickle','wb') as f:
	pickle.dump(state_dict, f)

with open('X_player.pickle','wb') as f:
	pickle.dump(state_dict, f)