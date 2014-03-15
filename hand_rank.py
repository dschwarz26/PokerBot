import classes
import utils

class Rank:
	def __init__(self, name, rank_values):
		self.name = name
		self.rank_values = rank_values
	
	hand_names = ['high_card', 'pair', 'two_pair', 'trips',
		      'straight', 'flush', 'full_house', 'quads', 'straight_flush']

	# is this __equals__ ?
	def equals(self, other):
		return self.name == other.name and self.rank_values == other.rank_values

	def compare_ranks(self, other):
		if self.hand_names.index(self.name) > self.hand_names.index(other.name):
			return 1
		if self.hand_names.index(self.name) < self.hand_names.index(other.name):
			return -1
		assert type(self.rank_values) == list and type(other.rank_values) == list, '%s %s %s %s' % (
			self.name, self.rank_values, other.name, other.rank_values)
		for i in range(len(self.rank_values)):
			if self.rank_values[i] > other.rank_values[i]:
				return 1
			if self.rank_values[i] < other.rank_values[i]:
				return -1
		return 0

	def _to_string(self):
		if self.name == 'straight_flush':
			return ('a straight flush, %s high' % classes._to_value(self.rank_values[0]))
		if self.name == 'quads':
			return ('four of a kind, %ss, %s kicker' % (
				classes._to_value(self.rank_values[0]),
				classes._to_value(self.rank_values[1])))
		if self.name == 'full_house':
			return ('a full house, %ss over %ss' % (
				classes._to_value(self.rank_values[0]),
				classes._to_value(self.rank_values[1])))
		if self.name == 'flush':
			return ('a flush, %s high' % classes._to_value(self.rank_values[0]))
		if self.name == 'straight':
			return ('a straight, %s high' % classes._to_value(self.rank_values[0]))
		if self.name == 'trips':
			return ('three of a kind, %ss, %s %s kicker' % (
				classes._to_value(self.rank_values[0]),
				classes._to_value(self.rank_values[1]),
				classes._to_value(self.rank_values[2])))
		if self.name == 'two_pair':
			return ('two pair, %ss and %ss, %s kicker' % (
				classes._to_value(self.rank_values[0]),
				classes._to_value(self.rank_values[1]),
				classes._to_value(self.rank_values[2])))
		if self.name == 'pair':
			return ('a pair of %ss, %s %s %s kicker' % (
				classes._to_value(self.rank_values[0]),
				classes._to_value(self.rank_values[1]),
				classes._to_value(self.rank_values[2]),
				classes._to_value(self.rank_values[3])))
		return ('high card %s, %s %s %s %s kicker' % (
				classes._to_value(self.rank_values[0]),
				classes._to_value(self.rank_values[1]),
				classes._to_value(self.rank_values[2]),
				classes._to_value(self.rank_values[3]),
				classes._to_value(self.rank_values[4]))) 

def order_ranks(ranks):
	return sorted(ranks, cmp = compare_ranks)

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
	if len(cards_by_suit[suit_with_max_number]) >= 5:
		counter = 0
		for x in classes.VALUES[::-1]:
			if x in cards_by_suit[suit_with_max_number]:
				counter += 1
				if counter  == 5:
					return Rank('straight_flush', [x + 4])
				#Special case for straight flush to the 5
				if x == 2 and counter == 4 and 14 in cards_by_suit[suit_with_max_number]:
					return Rank('straight_flush', [5])
			else:
				counter = 0
	
def get_rank_for_quads(cards_by_number):
	for x in cards_by_number:
		if cards_by_number[x] == 4:
			kicker = max(y for y in cards_by_number.keys() if cards_by_number[y] == 1)
			return Rank('quads', [x, kicker])
	 		
def get_rank_for_full_house(cards_by_number):
	trips = [x for x in cards_by_number if cards_by_number[x] == 3]
	if len(trips) == 2:
		return Rank('full_house', sorted(trips)[::-1])
	if len(trips) == 1:
		pairs = [x for x in cards_by_number if cards_by_number[x] == 2]
		if pairs:
			return Rank('full_house', [trips[0], max(pairs)])

def get_rank_for_flush(cards_by_suit, suit_with_max_number):
	if len(cards_by_suit[suit_with_max_number]) > 4:
		return Rank('flush', sorted(cards_by_suit[suit_with_max_number])[::-1][:5])

def get_rank_for_straight(cards_by_number):
	if cards_by_number[10] == 0 and cards_by_number[5] == 0:
		return None
	counter = classes.VALUES[-1]
	#Need to pop this key, value out of the dictionary after this method.
	cards_by_number[1] = cards_by_number[14]
	while True:
		five_cards_from_counter = [cards_by_number[counter - x] for x in range(5)]
		if 0 not in five_cards_from_counter:
			cards_by_number.pop(1)
			return Rank('straight', [counter])
		counter -= five_cards_from_counter.index(0) + 1
		if counter < 5:
			cards_by_number.pop(1)
			break

def get_rank_for_trips(cards_by_number):
	trips = [x for x in cards_by_number if cards_by_number[x] == 3]
	if trips:
		kickers = sorted([x for x in cards_by_number if cards_by_number[x] == 1])[::-1][:2]
		return Rank('trips', trips + kickers)

def get_rank_for_two_pair(cards_by_number):
	pairs = [x for x in cards_by_number if cards_by_number[x] == 2]
	if len(pairs) == 3:
		return Rank('two_pair', sorted(pairs)[::-1])
	if len(pairs) == 2:
		kicker = max(x for x in cards_by_number if cards_by_number[x] == 1)
		return Rank('two_pair', sorted(pairs)[::-1] + [kicker])

def get_rank_for_pair(cards_by_number):
	pairs = [x for x in cards_by_number if cards_by_number[x] == 2]
	if pairs:
		kickers = sorted([x for x in cards_by_number if cards_by_number[x] == 1])[::-1][:3]
		return Rank('pair', pairs + kickers)

def get_rank_for_high_card(cards_by_number):
	return Rank('high_card', 
		sorted([x for x in cards_by_number if cards_by_number[x] > 0])[::-1][:5])

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

