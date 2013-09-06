#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
random.seed()

VALUES = range(13)
RANKS = {9: 'J', 10: 'Q', 11: 'K', 12: 'A'}
SUITS = [u'♠',u'♥',u'♦',u'♣']

class Card:
	def __init__(self, value, suit):
		self.value = value
		self.suit = suit

	def _value_to_rank(self):
		if self.value < 9:
			return self.value + 2
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
		self.card_one, self.card_two = (None, None)

	def draw_hand(deck):
		self.card_one = deck.draw()
		self.card_two = deck.draw()

