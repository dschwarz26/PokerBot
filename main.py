import players
import deal

class Game:
	def __init__(self, player_names, stack_size, num_orbits=1):
		self.round_number = 0
		self.players = []
		self.num_orbits = num_orbits
		for name in player_names:
			self.players.append(players.RandomPlayer(stack_size, name))

	def play_game(self):
		dealer_seat = 0
		for _ in range(self.num_orbits):
			d = deal.Deal(self.players, dealer_seat=dealer_seat, debug_level=1)
			d.play_round()
			dealer_seat = (dealer_seat + 1) % len(self.players)

	def display_player_stats(self):
		print ("Hand %d" % self.round_number)
		for player in self.players:
			print ("Player %s has %d chips." % (player.name, player.chips))
		print ("-----------------------------")

if __name__ == '__main__':
	game = Game(['Alice', 'Bob', 'Charles'], 1000)
	game.play_game()
