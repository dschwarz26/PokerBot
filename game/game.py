import players
from deal import Deal
import utils

class Game:
	def __init__(self, players, stack_size=100, debug_level=1, num_orbits=1):
		self.round_number = 1
		self.players = []
		self.num_orbits = num_orbits
		self.debug_level = debug_level
		self.stack_size = stack_size
		for player in players:
			self.players.append(player)
		self.rebuys = [0 for player in self.players]

	def play_game(self):
		dealer_seat = 0
		for _ in range(self.num_orbits):
			for i, player in enumerate(self.players):
				if player.chips == 0:
					player.chips = self.stack_size
					self.rebuys[i] += 1
			self.display_player_stats()
			deal = Deal(self.players, dealer_seat=dealer_seat, debug_level=self.debug_level)
			deal.play_round()
			dealer_seat = (dealer_seat + 1) % len(self.players)
			self.round_number += 1

	def display_player_stats(self):
		utils.out('Hand %d' % self.round_number, self.debug_level)
		for player in self.players:
			utils.out('Player %s has %d chips.' % (player.name, player.chips), self.debug_level)
