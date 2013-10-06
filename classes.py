#!/usr/bin/python
# -*- coding: UTF-8 -*-

import hand_rank
import random
import utils
random.seed()

VALUES = range(2, 15)
RANKS = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
SUITS = [u'♠',u'♥',u'♦',u'♣']

class Card:
	def __init__(self, value, suit):
		self.value = value
		self.suit = suit

	def _value_to_rank(self):
		if self.value < 11:
			return self.value
		else:
			return RANKS[self.value]

	def read_out(self):
		return '%s%s' % (self._value_to_rank(), unicode(self.suit))

class Hand:
	def __init__(self, card_one, card_two):
		self.card_one = card_one
		self.card_two = card_two

	def read_out(self):
		return '%s %s' % (self.card_one.read_out(), self.card_two.read_out())

	def read_as_list(self):
		return [self.card_one, self.card_two]

class Deck:
	def __init__(self):
		self.cards = set()
		for value in VALUES:
			for suit in SUITS:
				self.cards.add(Card(value, suit))

	def draw(self, num_cards=1):
		try:
			cards = random.sample(self.cards, num_cards)
			for card in cards:
				self.cards.remove(card)
			return cards
		except ValueError:
			print("Drew too many cards.")
			return []

	def shuffle(self):
		self.__init__()

class Player:
	def __init__(self, chips, name):
		self.chips = chips
		self.name = name
		self.hand = None
		self.next_player = None
		self.has_acted = False
		self.in_hand = False
		self.all_in = False

	def draw_hand(self, deck):
		cards = deck.draw(2)
		self.hand = Hand(cards[0], cards[1])

	def get_player_n_seats(self, n):
		result = self
		for _ in range(n):
			result = result.next_player

class Round:
	def __init__(self, players, dealer_seat, small_blind, big_blind, debug_level=0):
		self.debug_level = debug_level	
		self.players = players
		self.deck = Deck()
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
			
	def play_round(self):
		self.pot += self.big_blind + self.small_blind
		self.players[self.get_next_active_seat(self.dealer_seat)].chips -= self.small_blind
		self.players[self.get_next_active_seat(self.dealer_seat, num_seats=2)].chips -= self.big_blind
		#Preflop
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
		#Turn
		self.communal_cards.append(self.deck.draw()[0])
		utils.out("Turn: %s" % self.communal_cards[3].read_out(), self.debug_level)
		seat_to_act = self.get_next_active_seat(self.dealer_seat)
		self.play_all_actions(seat_to_act)
		if self.num_players_in_hand <= 1:
			self.clean_up()
			return
		#River
		self.communal_cards.append(self.deck.draw()[0])
		utils.out("River: %s" % self.communal_cards[4].read_out(), self.debug_level)
		seat_to_act = self.get_next_active_seat(self.dealer_seat)
		self.play_all_actions(seat_to_act)
		self.clean_up(winners=self.get_winners())
	
	def get_winners(self):
		hands = {}
		seat = self.dealer_seat
		for _ in range(self.num_players_in_hand):
			if self.players[seat].in_hand:
				hands[self.players[seat].hand] = self.players[seat]
		winning_hands = hand_rank.compare_hands(self.communal_cards, [hand.read_as_list for hand in hands.keys()])
		winners = []
		for winning_hand in winning_hands:
			winners.append(hands[winning_hand])

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
                	self.players[seat_to_act] = self.get_action(seat_to_act)
                	seat_to_act = self.get_next_active_seat(seat_to_act)

	def get_action(self, seat):
		self.num_active_players_in_hand -= 1
		player = self.players[seat]
		action = ['call', 'raise', 'fold'][random.randint(0, 2)]
		utils.out("Player %s chooses to %s" % (player.name, action), self.debug_level)
		if action == 'call':
			player.chips -= self.bet
			self.pot += self.bet
			player.has_acted = True
			utils.out("Player %s now has %d chips. Pot is %d" % (
				player.name, player.chips, self.pot), self.debug_level)
			return player
		if action == 'raise':
			player.chips -= 2 * self.bet
			self.pot += 2 * self.bet
			self.bet = 2 * self.bet
			player.has_acted = True
			for _ in range(self.num_active_players_in_hand):
				seat = self.get_next_active_seat(seat)
				if self.players[seat].has_acted == False:
					self.players[seat].has_acted = True
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
		



