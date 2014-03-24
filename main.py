import players
import deal
import utils

class Game:
	def __init__(self, player_names, stack_size, debug_level=1, num_orbits=1):
		self.round_number = 1
		self.players = []
		self.num_orbits = num_orbits
		self.debug_level = debug_level
		for player in player_names:
			self.players.append(player['type'](stack_size, player['name']))
		self.rebuys = [0 for player in self.players]

	def play_game(self):
		dealer_seat = 0
		for _ in range(self.num_orbits):
			for i, player in enumerate(self.players):
				if player.chips == 0:
					player.chips = 1000
					self.rebuys[i] += 1
			self.display_player_stats()
			d = deal.Deal(self.players, dealer_seat=dealer_seat, debug_level=self.debug_level)
			d.play_round()
			dealer_seat = (dealer_seat + 1) % len(self.players)
			self.round_number += 1

	def display_player_stats(self):
		utils.out('Hand %d' % self.round_number, self.debug_level)
		for player in self.players:
			utils.out('Player %s has %d chips.' % (player.name, player.chips), self.debug_level)

if __name__ == '__main__':
	people = [
		{'name': 'Rando1', 'type': players.RandomPlayer},
		{'name': 'Rando2', 'type': players.RandomPlayer},
		{'name': 'Rando3', 'type': players.RandomPlayer},
		{'name': 'FoldoGuy', 'type': players.FoldPlayer},
		{'name': 'AllInGuy', 'type': players.AllInPlayer},
		{'name': 'CallGuy', 'type': players.CallPlayer}
	]
	game = Game(people, 1000, num_orbits = 100000, debug_level = 0)
	game.play_game()
	print ('Final stats:')
	for i, player in enumerate(game.players):
		print ('%s: %d' % (player.name, player.chips - 1000 * game.rebuys[i]))
	print(game.rebuys)
