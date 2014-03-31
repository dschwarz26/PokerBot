#!/usr/bin/python
# -*- coding: UTF-8 -*-

import hand_rank
import random
import utils
random.seed()

VALUES = range(2, 15)
SUITS = [u'♠',u'♥',u'♦',u'♣']

def _to_value(val):
	if val < 11:
		return val
	return {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}[val]

class Card:
	def __init__(self, value, suit):
		self.value = value
		if suit in SUITS:
			self.suit = suit
		else:
			self.suit = {'S': u'♠', 'H': u'♥', 'D': u'♦', "C": u'♣'}[suit]

	def read_out(self):
		return '%s%s' % (_to_value(self.value), unicode(self.suit))

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
		self.cards = [Card(value, suit) for value in VALUES for suit in SUITS]
		random.shuffle(self.cards)

	def draw(self, num_cards=1):
		try:
			return [self.cards.pop() for _ in range(num_cards)]
		except IndexError:
			print("Drew too many cards.")
			return []

	def shuffle(self):
		random.shuffle(self.cards)

class Player:
	def __init__(self, chips, name):
		self.chips = chips
		self.name = name
		self.hand = None
		self.rank = None
		self.has_acted = False
		self.in_hand = True
		self.all_in = False
		self.curr_bet = 0
		self.sidepot = None

	def draw_hand(self, deck):
		cards = deck.draw(2)
		self.hand = Hand(cards[0], cards[1])


