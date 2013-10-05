#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
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
		self.hand = [None, None]

	def draw_hand(deck):
		self.hand = deck.draw(2)

class Round:
	def __init__(self, players):
		self.players = players
		self.deck = Deck() 

	
	


