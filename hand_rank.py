#get tickets for eigsti and eldar!!

import math 

ranks = range(13)
suits = ['H', 'D', 'C', 'S']

hands = ['high_card', 'pair', 'two_pair', 'three_of_a_kind',
	'straight', 'flush', 'full_house', 'four_of_a_kind', 'straight_flush'] 

hand_rankings = dict(zip(hands, range(len(hands))))

class Card:
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit

def compare_hands(common_cards, hands):
	ranks_for_hands = {}
	for hand in hands:
		ranks_for_hands[hand] = get_rank(hand, common_cards)
	winning_hand = get_winner(ranks_for_hands)
	print ("Winner is %s with hand: %s" % (winner, hand))

def get_winner(ranks_for_hands):
	winning_hand = None
	for hand in ranks_for_hands.iterkeys():	
		if hand_comparison(hand, winner):
			winning_hand = hand
	return winning_hand

def hand_comparison(hand_one, hand_two):
	if hand_rankings[hand_one[0]] > hand_rankings[hand_two[0]]:
		return True
	if hand_one[0] == hand_two[0]:
		return hand_one[1] > hand_two[1]
	return False

def get_rank(hand, common_cards):
	cards = hand.union(common_cards)
	cards_by_rank = get_cards_by_rank(cards)
	cards_by_suit = get_cards_by_suit(cards)
	suit_with_max_number = max(cards_by_suit.iterkeys(), key=(lambda key:
		len(cards_by_suit[key])))
	rank_with_max_number = max(cards_by_rank.iterkeys(), key=(lambda key:
		cards_by_suit[key]))
	straight_flush = is_straight_flush(cards_by_suit)
	if straight_flush:
		return [hand_rankings["straight_flush"], straight_flush]
	four_of_a_kind = is_four_of_a_kind(cards_by_rank)
	if four_of_a_kind:
		return [hand_rankings["four_of_a_kind"], four_of_a_kind]
	full_house = is_full_house(cards_by_rank)
	if full_house:
		return [hand_rankings["full_house"], full_house]
	return ["high card", 5]
	
def is_straight_flush(cards_by_suit, suit_with_max_number):
	num_cards_in_suit = len(cards_by_suit(suit_with_max_number))
	if num_cards_in_suit < 5:
		return False
	for x in range(num_cards_in_suit) - 4:
		if has_straight_from_card(cards_by_suit(suit_with_max_number)):
			return cards_by_suit(suit_with_max_number)[x]
	return False

def is_four_of_a_kind(cards):
		

def is_full_house(cards):
	
		

def get_cards_by_suit(cards):
	cards_by_suit = {key: [] for key in suits}
	for card in cards:
		cards_by_suit[card.suit].append(card.rank)
	return cards_by_suit

def get_cards_by_rank(cards):
	cards_by_rank = {key: 0 for key in ranks}		
	for card in cards:
		cards_by_rank[card.rank] += 1
	return cards_by_rank

def has_straight_from_card(rank, ranks):
	for x in range(5):
		if not rank - x - 1 in ranks:
			return False
	return True



