import classes

class Rank:
	def __init__(self, name, rank_one, rank_two=None):
		self.name = name
		self.rank_one = rank_one
		self.rank_two = rank_two
	
	hand_names = ['high_card', 'pair', 'two_pair', 'trips',
		      'straight', 'flush', 'full_house', 'quads', 'straight_flush']

	def compare_ranks(self, rank):
		if hand_names.index(self.name) > hand_names.index(rank.name):
			return 1
		if hand_names.index(self.name) < hand_names.index(rank.name):
			return -1
		if self.rank_one > rank.rank_one:
			return 1
		if self.rank_one < rank.rank_one:
			return -1
		if self.rank_two > rank.rank_two:
			return 1
		if self.rank_two < rank.rank_two:
			return -1
		return 0

	def _to_string(self):
		return("%s %d %d" % (self.name, self.rank_one, self.rank_two) if self.rank_two else
			"%s %d" % (self.name, self.rank_one))

def compare_hands(common_cards, hands):
	ranks_for_hands = {}
	for hand in hands:
		ranks_for_hands[hand] = get_rank(hand.union(common_cards))
	winning_hands = get_winners(ranks_for_hands)
	print ("Winners are: ")
	for hand in winning_hands:
		print hand

def get_winners(ranks_for_hands):
	winning_hands = []
	winning_rank = Rank('high_card', 7)
	for hand in ranks_for_hands.iterkeys():
		rank = ranks_for_hands[hand]
		comparison = rank.compare_ranks(winning_rank)	
		if comparison == 1:
			winning_rank = rank
			winning_hands = [hand]
		elif comparison == 0:
			winning_hands.append(hand)
	return winning_hands

def get_rank(cards):
	cards_by_number = get_cards_by_number(cards)
	cards_by_suit = get_cards_by_suit(cards)
	suit_with_max_number = max(cards_by_suit.iterkeys(), key=(lambda key:
		len(cards_by_suit[key])))
	straight_flush = get_rank_for_straight_flush(cards_by_suit, suit_with_max_number)
	if straight_flush:
		return straight_flush
	quads = get_rank_for_quads(cards_by_number)
	if quads:
		return quads
	full_house = get_rank_for_full_house(cards_by_number)
	if full_house:
		return full_house
	flush = get_rank_for_flush(cards_by_suit, suit_with_max_number)
	if flush:
		return flush
	straight = get_rank_for_straight(cards_by_number)
	if straight:
		return straight
	trips = get_rank_for_trips(cards_by_number)
	if trips:
		return trips
	two_pair = get_rank_for_two_pair(cards_by_number)
	if two_pair:
		return two_pair
	pair = get_rank_for_pair(cards_by_number)
	if pair:
		return pair
	high_card = get_rank_for_high_card(cards_by_number)
	return high_card
	
def get_rank_for_straight_flush(cards_by_suit, suit_with_max_number):
	
	if  len(cards_by_suit[suit_with_max_number]) < 5:
		return None
	num_in_straight = 0
	for x in classes.VALUES[::-1]:
		if x in cards_by_suit[suit_with_max_number]:
			num_in_straight += 1
			if num_in_straight == 5:
				return Rank('straight_flush', x+4)
			if x == 2 and num_in_straight == 4 and 14 in cards_by_suit[suit_with_max_number]:
				return Rank('straight_flush', 5)
		else:
			num_in_straight = 0
	return None
	
def get_rank_for_quads(cards_by_number):
	for number in cards_by_number:
		if cards_by_number[number] == 4:
			return Rank('quads', number)
	return None
	 		
def get_rank_for_full_house(cards_by_number):
	trips = [number for number in cards_by_number if cards_by_number[number] == 3]
	if not trips:
		return None
	if len(trips) == 2:
		return Rank('full_house', sorted(trips)[1], sorted(trips)[0])
	pairs = [number for number in cards_by_number if cards_by_number[number] == 2]
	if not pairs:
		return None
	return Rank('full_house', trips[0], max(pairs)) 

def get_rank_for_flush(cards_by_suit, suit_with_max_number):
	if len(cards_by_suit[suit_with_max_number]) > 4:
		return Rank('flush', max(cards_by_suit[suit_with_max_number]))
	return None

def get_rank_for_straight(cards_by_number):
	if cards_by_number[10] == 0 and cards_by_number[5] == 0:
		return None
	counter = classes.VALUES[-1]
	cards_by_number_with_low_ace = cards_by_number
	cards_by_number_with_low_ace[1] = cards_by_number[14]
	while True:
		five_cards_from_counter = [cards_by_number_with_low_ace[counter - x] for x in range(5)]
		if 0 not in five_cards_from_counter:
			return Rank('straight', counter)
		counter -= five_cards_from_counter.index(0) + 1
		if counter < 5:
			return None

def get_rank_for_trips(cards_by_number):
	trips = [number for number in cards_by_number if cards_by_number[number] == 3]
	if not trips:
		return None
	return Rank('trips', max(trips))

def get_rank_for_two_pair(cards_by_number):
	pairs = [number for number in cards_by_number if cards_by_number[number] == 2]
	if len(pairs) < 2:
		return None
	return Rank('two_pair', sorted(pairs)[-1], sorted(pairs)[-2])

def get_rank_for_pair(cards_by_number):
	pairs = [number for number in cards_by_number if cards_by_number[number] == 2]
	if not pairs:
		return None
	return Rank('pair', max(pairs))

def get_rank_for_high_card(cards_by_number):
	return Rank('high_card', 
		max([number for number in cards_by_number if cards_by_number[number] > 0]))

def get_cards_by_suit(cards):
	cards_by_suit = {key: [] for key in classes.SUITS}
	for card in cards:
		cards_by_suit[card.suit].append(card.value)
	return cards_by_suit

def get_cards_by_number(cards):
	cards_by_number = {key: 0 for key in classes.VALUES}		
	for card in cards:
		cards_by_number[card.value] += 1
	return cards_by_number

