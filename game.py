import classes

class Game:
	def __init__(self, player_names, stack_size, num_orbits=1):
		self.round_number = 0
		self.players = []
		self.num_orbits = num_orbits
		for name in player_names:
			self.players.append(classes.Player(stack_size, name))

	def play_game(self):
		dealer_position = 0
		for _ in range(self.num_orbits):
			round_ = classes.Round(self.players, dealer_position, 1, 2, debug_level=2)
			round_.play_round()
			dealer_position = (dealer_position + 1) % len(self.players)

	def display_player_stats(self):
		print ("Hand %d" % self.round_number)
		for player in self.players:
			print ("Player %s has %d chips." % (player.name, player.chips))
		print ("-----------------------------")

game = Game(['Alice', 'Bob', 'Charles'], 1000)
game.play_game()
