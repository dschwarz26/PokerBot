import hand_rank
from classes import Card

hands = [
		["straight_flush", 8, None,
		[Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'S'),
		 Card(6, 'S'), Card(7, 'S'), Card(8, 'S')]],

		["straight", 8, None,
		[Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'S'),
		 Card(6, 'H'), Card(7, 'H'), Card(8, 'H')]],

		["flush", 9, None,
		[Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'S'),
		 Card(9, 'S'), Card(7, 'S'), Card(8, 'S')]],

		["high_card", 9, None,
		[Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'S'),
		 Card(9, 'H'), Card(7, 'D'), Card(8, 'C')]],

		["pair", 9, None,
		[Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'S'),
		 Card(9, 'D'), Card(9, 'H'), Card(8, 'C')]],

		["trips", 9, None,
		[Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'S'),
		 Card(9, 'H'), Card(9, 'D'), Card(9, 'C')]],

		["two_pair", 9, 8,
		[Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(8, 'H'),
		 Card(8, 'D'), Card(9, 'C'), Card(9, 'D')]],

		["two_pair", 9, 8,
		[Card(2, 'S'), Card(2, 'H'), Card(4, 'S'), Card(8, 'D'),
		 Card(8, 'C'), Card(9, 'S'), Card(9, 'C')]],

		["full_house", 9, 8,
		[Card(2, 'S'), Card(8, 'S'), Card(9, 'S'), Card(8, 'H'),
		 Card(9, 'H'), Card(8, 'D'), Card(9, 'D')]],

		["straight", 5, None,
		[Card(2, 'S'), Card(3, 'S'), Card(4, 'H'), Card(5, 'D'),
		 Card(14, 'H'), Card(7, 'D'), Card(8, 'S')]],

		["straight", 6, None,
		[Card(2, 'C'), Card(3, 'S'), Card(4, 'C'), Card(5, 'S'),
		 Card(6, 'S'), Card(6, 'H'), Card(6, 'D')]],

		["flush", 11, None,
		[Card(2, 'S'), Card(3, 'S'), Card(7, 'S'), Card(9, 'S'),
		 Card(11, 'S'), Card(11, 'H'), Card(11, 'D')]],
		
		["flush", 11, None,
		[Card(2, 'S'), Card(3, 'S'), Card(7, 'S'), Card(9, 'S'),
		 Card(11, 'S'), Card(11, 'H'), Card(11, 'D')]],
		
		["full_house", 9, 10,
		[Card(9, 'S'), Card(10, 'S'), Card(9, 'H'), Card(10, 'H'),
		 Card(9, 'D'), Card(11, 'H'), Card(12, 'D')]],

		["full_house", 9, 10,
		[Card(8, 'S'), Card(9, 'S'), Card(8, 'H'), Card(9, 'H'),
		 Card(10, 'S'), Card(9, 'D'), Card(10, 'D')]],

		["quads", 14, None,
		[Card(14, 'S'), Card(3, 'S'), Card(14, 'H'), Card(9, 'S'),
		 Card(14, 'D'), Card(11, 'H'), Card(14, 'C')]]
]

def test_get_rank():
	for hand in hands:
		expected_rank = hand_rank.Rank(hand[0], hand[1], hand[2])
		actual_rank = hand_rank.get_rank(hand[3])
		assert(expected_rank._to_string() == actual_rank._to_string())

if __name__ == '__main__':
	test_get_rank()
