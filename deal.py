import classes
import utils
import random

class Deal:
	def __init__(self, players, small_blind, big_blind, dealer_seat=0, debug_level=0):
		self.debug_level = debug_level	
		self.players = players
		self.deck = classes.Deck()
		for player in self.players:
			player.draw_hand(self.deck)
			player.in_hand = True
		self.dealer_seat = dealer_seat
		self.small_blind = small_blind
		self.big_blind = big_blind
		self.pot = 0
		self.bet = big_blind
		self.num_players_in_hand = len(self.players)
		self.num_active_players_in_hand = self.num_players_in_hand
		self.communal_cards = []

	def get_next_active_seat(self, seat, require_active=False, num_seats=1):
		result = seat
		for _ in range(num_seats):
			while True:
				result = (result + 1) % len(self.players)
				if result == seat:
					break
				if self.players[result].in_hand and (not require_active or not self.players[result].has_acted):
					break
	
		return result
	def initiate_round(self):
		self.pot += self.big_blind + self.small_blind

		seat_1 = self.get_next_active_seat(self.dealer_seat)
		seat_2 = self.get_next_active_seat(seat_1)

		small_blind = self.players[seat_1]
		small_blind.chips -= self.small_blind
		small_blind.curr_bet = self.small_blind
		self.players[seat_1] = small_blind
		#Perhaps players should have an update function?

		big_blind = self.players[seat_2]
		big_blind.chips -= self.big_blind
		big_blind.curr_bet = self.big_blind
		self.players[seat_2] = big_blind
		
	def play_round(self):
		self.initiate_round()
		
		#Preflop
		for player in self.players:
			utils.out("%s is dealt %s" % (player.name, player.hand.read_out()), self.debug_level)
                seat_to_act = self.get_next_active_seat(self.dealer_seat, num_seats=3)
		self.play_all_actions(seat_to_act)                
		if self.num_players_in_hand <= 1:
			self.clean_up()
			return
		#Flop
		flop_cards = self.deck.draw(num_cards=3)
		for card in flop_cards:
			self.communal_cards.append(card)
		utils.out("Flop: %s %s %s" % (self.communal_cards[0].read_out(), self.communal_cards[1].read_out(),
			self.communal_cards[2].read_out()), self.debug_level)
		seat_to_act = self.get_next_active_seat(self.dealer_seat)
		self.play_all_actions(seat_to_act)
		if self.num_players_in_hand <= 1:
			self.clean_up()
			return
		self.clean_up_betting_round()
		#Turn
		self.communal_cards.append(self.deck.draw()[0])
		self.num_active_players_in_hand = self.num_players_in_hand
		utils.out("Turn: %s" % self.communal_cards[3].read_out(), self.debug_level)
		seat_to_act = self.get_next_active_seat(self.dealer_seat)
		self.play_all_actions(seat_to_act)
		if self.num_players_in_hand <= 1:
			self.clean_up_round()
			return
		self.clean_up_betting_round()
		#River
		self.communal_cards.append(self.deck.draw()[0])
		self.num_active_players_in_hand = self.num_players_in_hand
		utils.out("River: %s" % self.communal_cards[4].read_out(), self.debug_level)
		seat_to_act = self.get_next_active_seat(self.dealer_seat)
		self.play_all_actions(seat_to_act)
		self.clean_up_round(winners=self.get_winners())
	
	def clean_up_betting_round(self):
		self.bet = 0
		self.pot = 0
		for player in self.players:
			player.curr_bet = 0
			player.has_acted = False

	def get_winners(self):
		hands = {}
		seat = self.dealer_seat
		for _ in range(self.num_players_in_hand):
			if self.players[seat].in_hand:
				hands[self.players[seat].hand] = self.players[seat]
			seat = self.get_next_active_seat(seat, require_active=False)
		winning_hands = hand_rank.compare_hands(self.communal_cards, hands.keys())
		winners = []
		for winning_hand in winning_hands:
			winners.append(hands[winning_hand])
		return winners

	def clean_up(self, winners=None):
		if winners:
			for winner in winners:
				winner.chips += self.pot / len(winners)
				utils.out("Player %s wins the pot of %d chips split %d ways with %s" % (
					winner.name, self.pot, len(winners), winner.hand.read_out()), self.debug_level)
		else:
			winner = self.players[self.dealer_seat]
			winner.chips += self.pot
			utils.out("Player %s wins the pot of %d with %s" % (
				winner.name, self.pot, winner.hand.read_out()), self.debug_level)

	def play_all_actions(self, seat_to_act):
		while self.num_active_players_in_hand > 0:
                	self.players[seat_to_act] = self.update_player_with_action(seat_to_act)
                	seat_to_act = self.get_next_active_seat(seat_to_act)	

	def get_action(self, seat):
		if self.bet == 0:
			return ['check', 'bet'][random.randint(0, 1)]
		if self.players[seat].curr_bet < self.bet:
			return ['call', 'raise', 'fold'][random.randint(0, 2)]
		#Remaing case is that it's preflop and the big blind has option.
		return ['check', 'raise'][random.randint(0, 1)]
		
	def update_player_with_action(self, seat):
		utils.out("Num active players: %d. " % self.num_active_players_in_hand, self.debug_level) 
		self.num_active_players_in_hand -= 1
		player = self.players[seat]
		action = self.get_action(seat)
		utils.out("%s %ss." % (player.name, action), self.debug_level)
		if action == 'bet':
			self.bet = 2
			player.has_acted = True
			player.curr_bet = self.bet
			player.chips -= self.bet
			utils.out("Player %s now has %d chips. Pot is %d" % (
				player.name, player.chips, self.pot), self.debug_level)
			return player

		if action == 'call':
			#Note: call_amount is 0 in the case that the big blind class preflop.
			call_amount = self.bet - player.curr_bet
			player.chips -= call_amount
			self.pot += call_amount
			player.has_acted = True
			utils.out("Player %s now has %d chips. Pot is %d" % (
				player.name, player.chips, self.pot), self.debug_level)
			return player
		if action == 'raise':
			#Temporary fixed raise amount of 2.
			raise_amount = self.bet - player.curr_bet + 2
			#To do: error message for illegal raise amount
			#TO DO: self.curr_raise is needed for raise bounds.
			self.bet = player.curr_bet + raise_amount
			player.chips -= raise_amount
			player.curr_bet += raise_amount
			self.pot += raise_amount
			player.has_acted = True
			#Every other player is now active in the hand.
			num_players_to_update = self.num_active_players_in_hand - 1
			for _ in range(num_players_to_update):
				seat = self.get_next_active_seat(seat)
				if self.players[seat].has_acted:
					self.players[seat].has_acted = False
					self.num_active_players_in_hand += 1
			utils.out("Player %s now has %d chips. Bet is %d. Pot is %d" % (
				player.name, player.chips, self.bet, self.pot), self.debug_level)
			return player
		if action == 'fold':
			player.in_hand = False
			self.num_players_in_hand -= 1
			if seat == self.dealer_seat:
				self.dealer_seat = self.get_next_active_seat(seat)
			return player	

