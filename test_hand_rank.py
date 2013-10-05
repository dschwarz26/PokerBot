import hand_rank
import classes

hands = [
		["straight_flush", 8, None,
		[classes.Card(2, classes.SUITS[0]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(4, classes.SUITS[0]), classes.Card(5, classes.SUITS[0]),
		 classes.Card(6, classes.SUITS[0]), classes.Card(7, classes.SUITS[0]),
		 classes.Card(8, classes.SUITS[0])]],

		["straight", 8, None,
		[classes.Card(2, classes.SUITS[0]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(4, classes.SUITS[0]), classes.Card(5, classes.SUITS[0]),
		 classes.Card(6, classes.SUITS[1]), classes.Card(7, classes.SUITS[1]),
		 classes.Card(8, classes.SUITS[1])]],

		["flush", 9, None,
		[classes.Card(2, classes.SUITS[0]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(4, classes.SUITS[0]), classes.Card(5, classes.SUITS[0]),
		 classes.Card(9, classes.SUITS[0]), classes.Card(7, classes.SUITS[0]),
		 classes.Card(8, classes.SUITS[0])]],

		["high_card", 9, None,
		[classes.Card(2, classes.SUITS[0]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(4, classes.SUITS[0]), classes.Card(5, classes.SUITS[0]),
		 classes.Card(9, classes.SUITS[1]), classes.Card(7, classes.SUITS[2]),
		 classes.Card(8, classes.SUITS[3])]],

		["pair", 9, None,
		[classes.Card(2, classes.SUITS[0]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(4, classes.SUITS[0]), classes.Card(5, classes.SUITS[0]),
		 classes.Card(9, classes.SUITS[2]), classes.Card(9, classes.SUITS[1]),
		 classes.Card(8, classes.SUITS[3])]],

		["trips", 9, None,
		[classes.Card(2, classes.SUITS[0]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(4, classes.SUITS[0]), classes.Card(5, classes.SUITS[0]),
		 classes.Card(9, classes.SUITS[1]), classes.Card(9, classes.SUITS[2]),
		 classes.Card(9, classes.SUITS[3])]],

		["two_pair", 9, 8,
		[classes.Card(2, classes.SUITS[0]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(4, classes.SUITS[0]), classes.Card(8, classes.SUITS[1]),
		 classes.Card(8, classes.SUITS[2]), classes.Card(9, classes.SUITS[3]),
		 classes.Card(9, classes.SUITS[2])]],

		["two_pair", 9, 8,
		[classes.Card(2, classes.SUITS[0]), classes.Card(2, classes.SUITS[1]),
		 classes.Card(4, classes.SUITS[0]), classes.Card(8, classes.SUITS[2]),
		 classes.Card(8, classes.SUITS[3]), classes.Card(9, classes.SUITS[0]),
		 classes.Card(9, classes.SUITS[3])]],

		["full_house", 9, 8,
		[classes.Card(2, classes.SUITS[0]), classes.Card(8, classes.SUITS[0]),
		 classes.Card(9, classes.SUITS[0]), classes.Card(8, classes.SUITS[1]),
		 classes.Card(9, classes.SUITS[1]), classes.Card(8, classes.SUITS[2]),
		 classes.Card(9, classes.SUITS[2])]],

		["straight", 5, None,
		[classes.Card(2, classes.SUITS[0]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(4, classes.SUITS[1]), classes.Card(5, classes.SUITS[2]),
		 classes.Card(14, classes.SUITS[1]), classes.Card(7, classes.SUITS[2]),
		 classes.Card(8, classes.SUITS[0])]],

		["straight", 6, None,
		[classes.Card(2, classes.SUITS[3]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(4, classes.SUITS[3]), classes.Card(5, classes.SUITS[0]),
		 classes.Card(6, classes.SUITS[0]), classes.Card(6, classes.SUITS[1]),
		 classes.Card(6, classes.SUITS[2])]],

		["flush", 11, None,
		[classes.Card(2, classes.SUITS[0]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(7, classes.SUITS[0]), classes.Card(9, classes.SUITS[0]),
		 classes.Card(11, classes.SUITS[0]), classes.Card(11, classes.SUITS[1]),
		 classes.Card(11, classes.SUITS[2])]],
		
		["flush", 11, None,
		[classes.Card(2, classes.SUITS[0]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(7, classes.SUITS[0]), classes.Card(9, classes.SUITS[0]),
		 classes.Card(11, classes.SUITS[0]), classes.Card(11, classes.SUITS[1]),
		 classes.Card(11, classes.SUITS[2])]],
		
		["full_house", 9, 10,
		[classes.Card(9, classes.SUITS[0]), classes.Card(10, classes.SUITS[0]),
		 classes.Card(9, classes.SUITS[1]), classes.Card(10, classes.SUITS[1]),
		 classes.Card(9, classes.SUITS[2]), classes.Card(11, classes.SUITS[1]),
		 classes.Card(12, classes.SUITS[2])]],

		["full_house", 9, 10,
		[classes.Card(8, classes.SUITS[0]), classes.Card(9, classes.SUITS[0]),
		 classes.Card(8, classes.SUITS[1]), classes.Card(9, classes.SUITS[1]),
		 classes.Card(10, classes.SUITS[0]), classes.Card(9, classes.SUITS[2]),
		 classes.Card(10, classes.SUITS[2])]],

		["quads", 14, None,
		[classes.Card(14, classes.SUITS[0]), classes.Card(3, classes.SUITS[0]),
		 classes.Card(14, classes.SUITS[1]), classes.Card(9, classes.SUITS[0]),
		 classes.Card(14, classes.SUITS[2]), classes.Card(11, classes.SUITS[1]),
		 classes.Card(14, classes.SUITS[3])]]
]

def test_get_rank():
	for hand in hands:
		expected_rank = hand_rank.Rank(hand[0], hand[1], hand[2])
		actual_rank = hand_rank.get_rank(hand[3])
		print ("Expected rank: " + expected_rank._to_string() + "   |   " +
			"Actual rank: " + actual_rank._to_string())

test_get_rank()
