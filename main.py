import sys

from game_manager import *
from player import *
from simple_rl_bot import *

def main(argv):
	if 'H' in argv:
		board = Board(verbose=True)
	else:
		board = Board()

	iterations = int(argv[2])
	
	player1 = get_player(argv[0], 'O')
	player2 = get_player(argv[1], 'X')

	for i in range(iterations):
		board.initialise_board()

		turn = player1

		while True:
			move = turn.get_move(board)
			board.make_move(move, turn.mark)

			if board.has_winner():
				print('Game ' + str(i+1) + ' over! Winner is: ' + turn.mark)
				turn.game_ended('win')
				other_player = player2 if turn == player1 else player1
				other_player.game_ended('loss')
				break

			elif board.has_draw():
				print('Game ' + str(i+1) + ' tied!')
				player1.game_ended('draw')
				player2.game_ended('draw')
				break

			turn = player2 if turn == player1 else player1

	print('All games done!')
	player1.all_done()
	player2.all_done()
	print(str(player1.num_draws) + ' draws, ' + str(player1.num_wins) + ' \'O\' wins, ' + str(player2.num_wins) + ' \'X\' wins.')

def get_player(player, mark):
	if player == 'H':
		return HumanPlayer(mark)

	elif player == 'S':
		return SimpleRlBot(mark, 0.001, mark + '_player.pickle')

if __name__ == '__main__':
	# command line usage: python3 filename.py player1 player2 num_iterations

	# H = Human, S = Simple
	valid_players = ['H', 'S']

	try:
		player1 = sys.argv[1].upper()
		player2 = sys.argv[2].upper()
	except:
		print('Usage: python3 filename.py player1 player2 number_of_games. players should be from: ' + str(valid_players))

	if player1 not in valid_players or player2 not in valid_players:
		print('Player is invalid. Must be one of ' + str(valid_players))


	main([player1, player2] + sys.argv[3:])