import classes
import hand_rank
import random

def restore_deck(deck, drawn_cards):
	for card in drawn_cards:
		deck.cards.append(card)
	deck.shuffle()

def simulate_hands(hand, communal_cards, deck, num_simulations):
	result = 0.0
	for _ in range(num_simulations):
		sample_cards = deck.draw(num_cards = 2)
		sample_hand = classes.Hand(sample_cards[0], sample_cards[1])
		additional_communal_cards = deck.draw(num_cards = 5 - len(communal_cards))
		final_communal_cards = communal_cards + additional_communal_cards
		sample_hand_rank = hand_rank.get_rank(sample_hand.read_as_list() + final_communal_cards)
		this_hand_rank = hand_rank.get_rank(hand.read_as_list() + final_communal_cards)
		comparison = hand_rank.Rank.compare_ranks(this_hand_rank, sample_hand_rank)
		if comparison == 1:
			result += 1
		elif comparison == 0:
			result += 0.5

		restore_deck(deck, sample_cards + additional_communal_cards)
	
	return result	
