import pickle

state_dict = {}

with open('./data_files/O_player.pickle','wb') as f:
	pickle.dump(state_dict, f)

with open('./data_files/X_player.pickle','wb') as f:
	pickle.dump(state_dict, f)