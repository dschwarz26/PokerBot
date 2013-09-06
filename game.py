import classes

class Game:
	def __init__(self, players, stack_size):
		self.round_number = 0
		self.players = players
		self.active_players = players
		for players in self.players:
			self.players.chips = stack_size

	def play_game(self):
		while len(self.active_players) > 1:
			dealer = self.active_players[0]
			hand = Hand(dealer, active_players)
			hand.play_hand()
			self.round_number += 1
			self.display_player_stats(self)
		winner = active_players[0]
		print("Game over.")
		print("The winner is %s after %d rounds with %d chips." % (
			winner.name, self.round_number, winner.chips)
		return

	def display_player_stats(self):
		print ("Hand %d" % self.round_number)
		for player in self.players:
			print ("Player %s has %d chips." % (player.name, player.chips))
		print ("-----------------------------")

class Hand(dealer, active_players):
	def __init__(self, dealer, active_players):
		self.deck = Deck()
		self.dealer = dealer
		self.players = active_players
		self.pot = 0

	def play_hand(self):
		for player in active_players:
			player.draw_hand(deck)
		players_in_hand = active_players
		run_preflop()
		run_flop()
		run_turn()
		run_river()

	def run_preflop(self):

	def run_flop(self):

	def run_turn(self):

	def run_river(self):	


