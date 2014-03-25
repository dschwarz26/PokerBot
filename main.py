import utils
import random

from game import Game
from players import *

player_types = [FoldPlayer, CallPlayer, AllInPlayer, RandomPlayer, TopPairPlayer, SmallSimulationPlayer] 
starting_chips = 200

#Returns a random set of players of size table_size
def get_players(table_size):
	players = []
	for i in range(table_size):
		player_type = random.choice(player_types)
		#Give each player a unique name.
		name = player_type.__name__ + str(i)
		player = player_type(starting_chips, name)
		players.append(player)
	return players

if __name__ == '__main__':
	results = {}
	for name in [player.__name__ for player in player_types]:
		results[name] = 0
	for _ in range(100):
		for table_size in range(3, 10):
			players = get_players(table_size)
			game = Game(players, stack_size = starting_chips, num_orbits = 100, debug_level = 0)
			game.play_game()
			for i, player in enumerate(game.players):
				#Track the results of each player type, so discard the id after the name.
				results[player.__name__.rstrip('1234567890')] += player.chips - starting_chips * game.rebuys[i]
	
	total_chips = 0
	for name, chips in results.iteritems():
		print 'Player type %s ends with %d' % (name, chips)
		total_chips += chips
	print 'Total chips: %d' % total_chips
