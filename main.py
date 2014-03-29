import utils
import random

from game import Game
from players import *

player_types = [RandomPlayer, RandomPlayer, RandomPlayer, RandomPlayer, RandomPlayer, RandomPlayer,
	SmallSimulationPlayer, SmallTAGSimulationPlayer, SmallLAGSimulationPlayer,
	LargeSimulationPlayer, LargeTAGSimulationPlayer, LargeLAGSimulationPlayer,
	TAGPlayer, TightTAGPlayer, LooseTAGPlayer] 

#Returns a random set of players of size table_size
def get_players(table_size, starting_chips, results):
	players = []
	for i in range(table_size):
		player_type = random.choice(player_types)
		#Give each player a unique name.
		name = player_type.__name__ + str(i)
		player = player_type(starting_chips, name)
		players.append(player)
		results[player_type.__name__]['num_instances'] += 1
	return players, results

def tally_results(results_for_player, starting_chips):
	return results_for_player['final_chips'] - starting_chips * (
		results_for_player['num_instances'] + results_for_player['num_rebuys'])

if __name__ == '__main__':
	starting_chips = 200
	num_iterations = 250
	num_orbits = 20
	table_sizes = range(3, 10)
	results = {}
	for name in [player.__name__ for player in player_types]:
		results[name] = {'final_chips': 0, 'num_instances': 0, 'num_rebuys': 0, 'result': 0}
	for _ in range(num_iterations):
		for table_size in table_sizes:
			players, results = get_players(table_size, starting_chips, results)
			game = Game(players, stack_size = starting_chips, num_orbits = num_orbits, debug_level = 0)
			game.play_game()
			for i, player in enumerate(game.players):
				#Discard identifying string appended to name to track each player type
				name = player.__name__.rstrip('1234567890')
				results[name]['final_chips'] += player.chips
				results[name]['num_rebuys'] += game.rebuys[i]
	print results
	total_chips = 0
	for name in results.keys():
		results[name]['result'] = tally_results(results[name], starting_chips)
	for name in sorted(results.keys(), key = lambda x: results[x]['result']):
		print '%s ends with %d. Instances: %d, rebuys: %d' % (name,
			results[name]['result'], results[name]['num_instances'], results[name]['num_rebuys'])
		total_chips += results[name]['result']
	print 'Total chips: %d' % total_chips
