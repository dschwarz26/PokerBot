from classes import Deck
import utils
import hand_rank

class Deal:
	def __init__(self, players, small_blind=1, big_blind=2, dealer_seat=0, debug_level=0):
		self.debug_level = debug_level	
		self.players = players
		self.deck = Deck()
		for player in self.players:
			player.draw_hand(self.deck)
			player.in_hand = True
			player.curr_bet = 0
			player.all_in = False
			player.has_acted = False
		self.small_blind_seat = self.get_next_seat(dealer_seat)
		self.small_blind = small_blind
		self.big_blind = big_blind
		self.pot = 0
		self.curr_raise = 0
		self.num_players_in_hand = len(self.players)
		self.num_active_players_in_hand = self.num_players_in_hand
		self.communal_cards = []

		utils.out('---------------------------------------', self.debug_level)
		utils.out('%s(%d) is dealer.' % (self.players[dealer_seat].name, self.players[dealer_seat].chips),
			self.debug_level)
	
	def get_next_seat(self, seat, require_active=True, num_seats=1):
		result = seat
		if num_seats > 1:
			for _ in range(num_seats):
				seat = self.get_next_seat(seat, require_active=require_active)
			return seat	
		for i in range(len(self.players)):
				result = (result + 1) % len(self.players)
				if (self.players[result].in_hand and
				   (not require_active or 
					(not self.players[result].has_acted and not self.players[result].all_in))):
					return result
		return seat
		
	def set_all_other_players_active(self, seat):
		for _ in range(self.num_players_in_hand - 1):
			seat = self.get_next_seat(seat, require_active = False)
	 		if not self.players[seat].all_in and self.players[seat].has_acted:
				self.players[seat].has_acted = False
				self.num_active_players_in_hand += 1


	def initiate_round(self):
		self.pot = self.big_blind + self.small_blind
		self.bet = self.big_blind
		self.players[self.small_blind_seat].chips -= self.small_blind
		self.players[self.small_blind_seat].curr_bet = self.small_blind
		utils.out('%s(%d) posts small blind of %d.' % (
			self.players[self.small_blind_seat].name,
			self.players[self.small_blind_seat].chips, self.small_blind),
			self.debug_level)

		big_blind_seat = self.get_next_seat(self.small_blind_seat)
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
                seat_to_act = self.get_next_seat(self.small_blind_seat, num_seats=2)
		if self.play_all_actions(seat_to_act):
			return                
		self.clean_up_betting_round()
		
		#Flop
		self.communal_cards += self.deck.draw(num_cards=3)
		utils.out("Flop: %s %s %s" % (self.communal_cards[0].read_out(), self.communal_cards[1].read_out(),
			self.communal_cards[2].read_out()), self.debug_level)
		if self.play_all_actions(self.small_blind_seat):
			return
		self.clean_up_betting_round()
		
		#Turn
		self.communal_cards += self.deck.draw()
		utils.out("Turn: %s" % self.communal_cards[3].read_out(), self.debug_level)
		if self.play_all_actions(self.small_blind_seat):
			return
		self.clean_up_betting_round()

		#River
		self.communal_cards += self.deck.draw()
		utils.out("River: %s" % self.communal_cards[4].read_out(), self.debug_level)
		if self.play_all_actions(self.small_blind_seat):
			return
		self.clean_up(winners=self.get_winners())
	
	def clean_up_betting_round(self):
		for player in self.players:
			player.curr_bet = 0
			player.has_acted = False
		self.bet = 0
		self.curr_raise = 0
		self.num_active_players_in_hand = self.num_players_in_hand		

	def get_players_by_rank(self):
		#TO DO: make a method for iterating through the players
		players_in_hand = []
		seat = self.small_blind_seat
		for _ in range(self.num_players_in_hand):
			if self.players[seat].in_hand:
				players_in_hand.append(self.players[seat])
				self.players[seat].rank = hand_rank.get_rank(
					self.players[seat].hand.read_as_list() + self.communal_cards)
				utils.out('%s(%s) has %s' % (self.players[seat].name,
					self.players[seat].hand.read_out(), self.players[seat].rank._to_string()), self.debug_level)
			seat = self.get_next_seat(seat, require_active = False)
		
		players_by_rank = sorted(players_in_hand, key = lambda x: x.rank, cmp = hand_rank.Rank.compare_ranks)
		return players_by_rank

	# If the hand went to showdown, show the winning cards and pay out the pot. If
	# not, the pot goes to the last remaining player in the hand.
	def clean_up(self, players_by_rank=None, winning_seat=None):
		#Hand did not go to showdown
		#winning_seat may be 0
		if winning_seat is not None:
			winner = self.players[winning_seat]
			winner.chips += self.pot
			utils.out("%s(%d) wins the pot of %d" % (
				winner.name, winner.chips, self.pot), self.debug_level)
		#Hand went to showdown
		else:
			while self.pot > 0:
				winner = players_by_rank.pop()
				if winner.sidepot:
					winnings = winner.sidepot
				else:
					winnings = self.pot
				self.pot -= winnings
				winner.chips += winnings
				utils.out("%s(%d) wins %d chips with %s" % (
					winner.name, winner.chips, winnings, winner.hand.read_out()), self.debug_level)
	
	def go_to_showdown(self):
		num_cards = len(self.communal_cards)
		self.communal_cards += self.deck.draw(num_cards = 5 - num_cards)
		if not num_cards:
			utils.out("Flop: %s %s %s" % (self.communal_cards[0].read_out(), self.communal_cards[1].read_out(),
				self.communal_cards[2].read_out()), self.debug_level)
			utils.out("Turn: %s" % self.communal_cards[3].read_out(), self.debug_level)
			utils.out("River: %s" % self.communal_cards[4].read_out(), self.debug_level)
		elif num_cards == 3:
			utils.out("Turn: %s" % self.communal_cards[3].read_out(), self.debug_level)
			utils.out("River: %s" % self.communal_cards[4].read_out(), self.debug_level)
		elif num_cards == 4:	
			utils.out("River: %s" % self.communal_cards[4].read_out(), self.debug_level)
		
	#Loops through the players and plays their actions. If the hand ends during the loop, return
	#True, otherwise return False.
	def play_all_actions(self, seat_to_act):
		while self.num_active_players_in_hand > 0:
			action = self.players[seat_to_act].get_action(self)
                	self.players[seat_to_act] = self.update_player_with_action(seat_to_act, action)
			#If, after this player's action, there is only one remaining player in the
			#hand, find that player and declare them the winner.
			if self.num_players_in_hand == 1:
				for i, player in enumerate(self.players):
					if player.in_hand:
						self.clean_up(winning_seat = i)
				return True
			if self.num_active_players_in_hand > 0:
                		seat_to_act = self.get_next_seat(seat_to_act)	
		for player in self.players:
			if player.in_hand:
				if player.all_in and not player.sidepot:
					self.update_player_with_sidepot(player)
		#If at least all but one player in the hand is all in, run the remaining
		#communal cards and go to showdown.
		if len([player for player in self.players if player.all_in]) >= self.num_players_in_hand - 1:
			self.go_to_showdown()
			self.clean_up(players_by_rank = self.get_players_by_rank())
			return True
		return False
	
	def update_player_with_check(self, player):
		utils.out('%s(%d) checks.' % (player.name, player.chips), self.debug_level)

	def update_player_with_bet(self, player, bet_size):
		self.bet = bet_size
		player.curr_bet += self.bet
		player.chips -= self.bet
		self.pot += self.bet
		utils.out("%s(%d) bets %d. Pot is %d" % (
		player.name, player.chips, self.bet, self.pot), self.debug_level)

	def update_player_with_call(self, player):
		#Note: call_amount is 0 in the case that the big blind calls preflop.
		amount_to_call = self.bet - player.curr_bet
		#Check if player is all-in
		if amount_to_call > player.chips:
			player.curr_bet += player.chips
			player.chips = 0
			self.pot += player.chips
		else:
			player.curr_bet = self.bet
			player.chips -= amount_to_call
			self.pot += amount_to_call
		utils.out("%s(%d) calls for %d. Pot is %d" % (
			player.name, player.chips, amount_to_call, self.pot), self.debug_level)
			
	def update_player_with_raise(self, player, raise_increase):
		amount_to_call = self.bet - player.curr_bet
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
	
	#Calculates the sidepot for a player as follows. For each other player in the hand,
	#add chips equal to the player's all-in bet, or add chips based on the other player's
	#all-in bet, whichever is lower.
	def update_player_with_sidepot(self, player):
		player.sidepot = player.curr_bet
		for curr_player in self.players:
			#To do: players cannot have the same name
			if curr_player.name != player.name:
				if curr_player.curr_bet < player.curr_bet:
					player.sidepot += curr_player.curr_bet
				else:
					player.sidepot += player.curr_bet
		utils.out('%s has a sidepot of %d' % (player.name, player.sidepot), self.debug_level)
		return player

	#The action parameter stores as first index the name of the action, and as an optional
	#second index the size of the bet or raise.
	def update_player_with_action(self, seat, action):
		self.num_active_players_in_hand -= 1
		player = self.players[seat]
		player.has_acted = True
		if action[0] == 'check':
			self.update_player_with_check(player)
		if action[0] == 'bet':
			self.update_player_with_bet(player, action[1])
			self.set_all_other_players_active(seat)	
		if action[0] == 'call':
			self.update_player_with_call(player)
		if action[0] == 'raise':
			self.update_player_with_raise(player, action[1])
			self.set_all_other_players_active(seat)
		if player.chips == 0:
			player.all_in = True
		if action[0] == 'fold':
			self.update_player_with_fold(player)
			#If the player who folded is the first to act, the next active player is now first to act.
			if seat == self.small_blind_seat:
				self.small_blind_seat = self.get_next_seat(seat, require_active = False)
		return player
			
