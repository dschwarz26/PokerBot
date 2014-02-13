import classes
import utils
import random
import hand_rank

class Deal:
	def __init__(self, players, small_blind=1, big_blind=2, dealer_seat=0, debug_level=0):
		self.debug_level = debug_level	
		self.players = players
		self.deck = classes.Deck()
		for player in self.players:
			player.draw_hand(self.deck)
			player.in_hand = True
			player.curr_bet = 0
		self.dealer_seat = dealer_seat
		self.small_blind = small_blind
		self.big_blind = big_blind
		self.pot = 0
		self.curr_raise = 0
		self.num_players_in_hand = len(self.players)
		self.num_active_players_in_hand = self.num_players_in_hand
		self.communal_cards = []

	def get_next_active_seat(self, seat, require_active=False, num_seats=1):
		result = seat
		if num_seats > 1:
			for _ in range(num_seats):
				seat = self.get_next_active_seat(seat, require_active=require_active)
			return seat	
		for i in range(len(self.players)):
				result = (result + 1) % len(self.players)
				if (self.players[result].in_hand and
				   (not require_active or not self.players[result].has_acted)):
					return result
		return seat

	def initiate_round(self):
		self.pot = self.big_blind + self.small_blind
		self.bet = self.big_blind

		utils.out('%s(%d) is dealer.' % (self.players[self.dealer_seat].name, self.players[self.dealer_seat].chips),
			self.debug_level)

		small_blind_seat = self.get_next_active_seat(self.dealer_seat)
		big_blind_seat = self.get_next_active_seat(small_blind_seat)

		self.players[small_blind_seat].chips -= self.small_blind
		self.players[small_blind_seat].curr_bet = self.small_blind
		utils.out('%s(%d) posts small blind of %d.' % (
			self.players[small_blind_seat].name, self.players[small_blind_seat].chips, self.small_blind),
			self.debug_level)

		self.players[big_blind_seat].chips -= self.big_blind
		self.players[big_blind_seat].curr_bet = self.big_blind
		utils.out('%s(%d) posts big blind of %d.' % (
			self.players[big_blind_seat].name, self.players[big_blind_seat].chips, self.big_blind),
			self.debug_level)

	def play_round(self):
		self.initiate_round()
		
		#Preflop
		for player in self.players:
			utils.out("%s is dealt %s" % (player.name, player.hand.read_out()), self.debug_level)
                seat_to_act = self.get_next_active_seat(self.dealer_seat, num_seats=3)
		if self.play_all_actions(seat_to_act):
			return                
		self.clean_up_betting_round()
		#Flop
		flop_cards = self.deck.draw(num_cards=3)
		for card in flop_cards:
			self.communal_cards.append(card)
		utils.out("Flop: %s %s %s" % (self.communal_cards[0].read_out(), self.communal_cards[1].read_out(),
			self.communal_cards[2].read_out()), self.debug_level)
		seat_to_act = self.get_next_active_seat(self.dealer_seat)
		if self.play_all_actions(seat_to_act):
			return
		self.clean_up_betting_round()
		#Turn
		self.communal_cards.append(self.deck.draw()[0])
		self.num_active_players_in_hand = self.num_players_in_hand
		utils.out("Turn: %s" % self.communal_cards[3].read_out(), self.debug_level)
		seat_to_act = self.get_next_active_seat(self.dealer_seat)
		if self.play_all_actions(seat_to_act):
			return
		self.clean_up_betting_round()
		#River
		self.communal_cards.append(self.deck.draw()[0])
		self.num_active_players_in_hand = self.num_players_in_hand
		utils.out("River: %s" % self.communal_cards[4].read_out(), self.debug_level)
		seat_to_act = self.get_next_active_seat(self.dealer_seat)
		if self.play_all_actions(seat_to_act):
			return
		self.clean_up(winners=self.get_winners())
	
	def clean_up_betting_round(self):
		self.bet = 0
		self.curr_raise = 0
		self.num_active_players_in_hand = self.num_players_in_hand
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
		winning_hands = classes.hand_rank.compare_hands(self.communal_cards, hands.keys())
		winners = []
		for winning_hand in winning_hands:
			winners.append(hands[winning_hand])
		utils.out('Winners are: %s' % ', '.join([player.name for player in winners]), self.debug_level)
		return winners

	# If the hand went to showdown, show the winning cards and pay out the pot. If
	# not, the pot goes to the last remaining player in the hand.
	def clean_up(self, winners=None, winning_seat=None):
		if winners:
			for winner in winners:
				winner.chips += self.pot / len(winners)
				utils.out("%s(%d) wins the pot of %d split %d ways with %s" % (
					winner.name, winner.chips, self.pot, len(winners), winner.hand.read_out()), self.debug_level)
		else:
			winner = self.players[winning_seat]
			winner.chips += self.pot
			utils.out("%s(%d) wins the pot of %d" % (
				winner.name, winner.chips, self.pot), self.debug_level)

	#Loops through the players and plays their actions. If the hand ends during the loop, return
	#True, otherwise return False.
	def play_all_actions(self, seat_to_act):
		while self.num_active_players_in_hand > 0:
                	self.players[seat_to_act] = self.update_player_with_action(seat_to_act)
			#If, after this player's action, there is only one remaining player in the
			#hand, find that player and declare them the winner.
			if self.num_players_in_hand == 1:
				for i, player in enumerate(self.players):
					if player.in_hand:
						self.clean_up(winning_seat = i)
				return True
			if self.num_active_players_in_hand > 0:
                		seat_to_act = self.get_next_active_seat(seat_to_act)	
		return False

	#Currently picks a random action for each player.
	def get_action(self, seat):
		#to do: implement all-in tag
		if self.bet == 0:
			return ['check', 'bet'][random.randint(0, 1)]
		if self.players[seat].curr_bet < self.bet:
			if self.players[seat].chips <= self.bet - self.players[seat].curr_bet:
				return ['call', 'fold'][random.randint(0, 1)]
			else:
				return ['call', 'raise', 'fold'][random.randint(0, 2)]
		#Remaing case is that it's preflop and the big blind has option.
		return ['check', 'raise'][random.randint(0, 1)]
		
	def set_all_other_players_active(self, seat):
		seat_to_update = seat
		self.num_active_players_in_hand = self.num_players_in_hand - 1
		for _ in range(self.num_active_players_in_hand):
			seat_to_update = self.get_next_active_seat(seat_to_update)
	 		self.players[seat_to_update].has_acted = False

	def update_player_with_check(self, player):
		utils.out('%s(%d) checks.' % (player.name, player.chips), self.debug_level)

	def update_player_with_bet(self, player):
		min_bet = self.big_blind
		max_bet = player.chips
		self.bet = random.randint(min_bet, max_bet)
		player.curr_bet += self.bet
		player.chips -= self.bet
		self.pot += self.bet
		utils.out("%s(%d) bets %d. Pot is %d" % (
		player.name, player.chips, self.bet, self.pot), self.debug_level)

	def update_player_with_call(self, player):
		#Note: call_amount is 0 in the case that the big blind calls preflop.
		amount_to_call = self.bet - player.curr_bet
		player.curr_bet = self.bet
		player.chips -= amount_to_call
		self.pot += amount_to_call
		utils.out("%s(%d) calls for %d. Pot is %d" % (
			player.name, player.chips, amount_to_call, self.pot), self.debug_level)
			
	def update_player_with_raise(self, player):
		amount_to_call = self.bet - player.curr_bet
		max_raise_increase = player.chips - amount_to_call
		min_raise_increase = self.curr_raise if self.curr_raise else self.bet
		raise_increase = (random.randint(min_raise_increase, max_raise_increase)
			if min_raise_increase < max_raise_increase
			else max_raise_increase) 
		player.chips -= amount_to_call + raise_increase
		self.bet += raise_increase
		player.curr_bet = self.bet
		self.pot += amount_to_call + raise_increase
		self.curr_raise += raise_increase
		utils.out("%s(%d) raises to %d. Pot is %d" % (
			player.name, player.chips, self.bet, self.pot), self.debug_level)

	def update_player_with_fold(self, player):
		player.in_hand = False
		self.num_players_in_hand -= 1
		utils.out('%s(%d) folds.' % (
			player.name, player.chips), self.debug_level)
			
	def update_player_with_action(self, seat):
		self.num_active_players_in_hand -= 1
		player = self.players[seat]
		action = self.get_action(seat)
		player.has_acted = True
		if action == 'check':
			self.update_player_with_check(player)
		if action == 'bet':
			self.update_player_with_bet(player)
			self.set_all_other_players_active(seat)	
		if action == 'call':
			self.update_player_with_call(player)
		if action == 'raise':
			self.update_player_with_raise(player)
			self.set_all_other_players_active(seat)
		if action == 'fold':
			self.update_player_with_fold(player)
			#If the player who folded is the dealer, the next active player is the new dealer.
			if seat == self.dealer_seat:
				self.dealer_seat = self.get_next_active_seat(seat)
		return player
			
