#!/usr/bin/python
# -*- coding: UTF-8 -*-
import classes

def print_cards(cards):
	print ' '.join([card.read_out() for card in cards])
	#for card in cards:
	#	print card.read_out()

deck = classes.Deck()
cards = deck.draw()
print_cards(cards)
deck.shuffle()
cards = deck.draw(10)
print_cards(cards)
deck.shuffle()
cards = deck.draw(100)
print_cards(cards)
deck.shuffle()
cards = deck.draw(2)
print_cards(cards)
cards = deck.draw(2)
print_cards(cards)
cards = deck.draw(50)
print_cards(cards)



