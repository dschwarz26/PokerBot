import unittest
import hand_rank

from classes import Card

hands = [
		{'expected': 
			{'name': 'straight_flush',
			 'rank_values': [8]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'S'),
		 	 Card(6, 'S'), Card(7, 'S'), Card(8, 'S')]
		},
		{'expected': 
			{'name': 'straight_flush',
			 'rank_values': [5]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'S'),
		 	 Card(6, 'H'), Card(7, 'H'), Card(14, 'S')]
		},
		{'expected': 
			{'name': 'straight_flush',
			 'rank_values': [14]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(14, 'S'), Card(10, 'S'),
		 	 Card(11, 'S'), Card(12, 'S'), Card(13, 'S')]
		},
		{'expected': 
			{'name': 'straight_flush',
			 'rank_values': [8]
			},
		 'cards': 
			[Card(2, 'H'), Card(3, 'H'), Card(4, 'S'), Card(5, 'S'),
		 	 Card(6, 'S'), Card(7, 'S'), Card(8, 'S')]
		},
		{'expected': 
			{'name': 'flush',
			 'rank_values': [8, 7, 6, 4, 3]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'H'),
		 	 Card(6, 'S'), Card(7, 'S'), Card(8, 'S')]
		},
		{'expected': 
			{'name': 'flush',
			 'rank_values': [10, 7, 5, 4, 3]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(4, 'S'), Card(5, 'S'),
		 	 Card(7, 'S'), Card(10, 'S'), Card(11, 'H')]
		},
		{'expected': 
			{'name': 'flush',
			 'rank_values': [14, 9, 8, 7, 6]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(9, 'S'), Card(6, 'S'),
		 	 Card(7, 'S'), Card(8, 'S'), Card(14, 'S')]
		},
		{'expected': 
			{'name': 'flush',
			 'rank_values': [14, 10, 8, 6, 2]
			},
		 'cards': 
			[Card(2, 'S'), Card(4, 'H'), Card(6, 'S'), Card(8, 'S'),
		 	 Card(10, 'S'), Card(12, 'D'), Card(14, 'S')]
		},
		{'expected': 
			{'name': 'straight',
			 'rank_values': [8]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'D'), Card(4, 'C'), Card(5, 'S'),
		 	 Card(6, 'S'), Card(7, 'D'), Card(8, 'C')]
		},
		{'expected': 
			{'name': 'straight',
			 'rank_values': [5]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'C'), Card(4, 'H'), Card(5, 'S'),
		 	 Card(8, 'S'), Card(7, 'C'), Card(14, 'H')]
		},

		{'expected': 
			{'name': 'straight',
			 'rank_values': [14]
			},
		 'cards': 
			[Card(2, 'S'), Card(10, 'H'), Card(9, 'C'), Card(11, 'C'),
		 	 Card(12, 'S'), Card(13, 'S'), Card(14, 'S')]
		},
		{'expected': 
			{'name': 'straight',
			 'rank_values': [8]
			},
		 'cards': 
			[Card(11, 'S'), Card(10, 'D'), Card(4, 'C'), Card(5, 'S'),
		 	 Card(6, 'S'), Card(7, 'D'), Card(8, 'C')]
		},
		{'expected': 
			{'name': 'full_house',
			 'rank_values': [8, 7]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(7, 'C'), Card(7, 'H'),
		 	 Card(8, 'S'), Card(8, 'C'), Card(8, 'D')]
		},
		{'expected': 
			{'name': 'full_house',
			 'rank_values': [8, 7]
			},
		 'cards': 
			[Card(2, 'S'), Card(2, 'C'), Card(7, 'C'), Card(7, 'S'),
		 	 Card(8, 'H'), Card(8, 'C'), Card(8, 'D')]
		},
		{'expected': 
			{'name': 'full_house',
			 'rank_values': [7, 8]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(7, 'S'), Card(7, 'S'),
		 	 Card(7, 'H'), Card(8, 'C'), Card(8, 'S')]
		},

		{'expected': 
			{'name': 'full_house',
			 'rank_values': [14, 13]
			},
		 'cards': 
			[Card(2, 'S'), Card(13, 'D'), Card(13, 'C'), Card(13, 'S'),
		 	 Card(14, 'S'), Card(14, 'D'), Card(14, 'C')]
		},
		{'expected': 
			{'name': 'trips',
			 'rank_values': [8, 7, 6]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(6, 'S'), Card(7, 'S'),
		 	 Card(8, 'D'), Card(8, 'C'), Card(8, 'H')]
		},
		{'expected': 
			{'name': 'trips',
			 'rank_values': [8, 14, 12]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(14, 'C'), Card(12, 'H'),
		 	 Card(8, 'H'), Card(8, 'S'), Card(8, 'D')]
		},
		{'expected': 
			{'name': 'trips',
			 'rank_values': [3, 10, 5]
			},
		 'cards': 
			[Card(3, 'C'), Card(3, 'D'), Card(3, 'H'), Card(10, 'S'),
		 	 Card(2, 'S'), Card(4, 'S'), Card(5, 'H')]
		},
		{'expected': 
			{'name': 'trips',
			 'rank_values': [14, 13, 12]
			},
		 'cards': 
			[Card(12, 'C'), Card(13, 'H'), Card(14, 'D'), Card(14, 'S'),
		 	 Card(9, 'D'), Card(10, 'S'), Card(14, 'C')]
		},

		{'expected': 
			{'name': 'two_pair',
			 'rank_values': [3, 2, 10]
			},
		 'cards': 
			[Card(2, 'S'), Card(2, 'H'), Card(3, 'S'), Card(3, 'H'),
		 	 Card(8, 'S'), Card(9, 'S'), Card(10, 'H')]
		},
		{'expected': 
			{'name': 'two_pair',
			 'rank_values': [10, 9, 8]
			},
		 'cards': 
			[Card(2, 'S'), Card(8, 'H'), Card(8, 'S'), Card(9, 'C'),
		 	 Card(9, 'S'), Card(10, 'D'), Card(10, 'H')]
		},
		{'expected': 
			{'name': 'two_pair',
			 'rank_values': [14, 13, 6]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'H'), Card(6, 'S'), Card(13, 'H'),
		 	 Card(13, 'C'), Card(14, 'D'), Card(14, 'D')]
		},
		{'expected': 
			{'name': 'two_pair',
			 'rank_values': [14, 2, 9]
			},
		 'cards': 
			[Card(2, 'S'), Card(2, 'C'), Card(14, 'S'), Card(14, 'D'),
		 	 Card(6, 'H'), Card(7, 'C'), Card(9, 'S')]
		},
		{'expected': 
			{'name': 'pair',
			 'rank_values': [8, 7, 6, 5]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'C'), Card(5, 'H'), Card(6, 'S'),
		 	 Card(7, 'S'), Card(8, 'C'), Card(8, 'S')]
		},

		{'expected': 
			{'name': 'pair',
			 'rank_values': [8, 13, 10, 6]
			},
		 'cards': 
			[Card(2, 'S'), Card(6, 'H'), Card(8, 'H'), Card(8, 'S'),
		 	 Card(13, 'S'), Card(10, 'C'), Card(3, 'S')]
		},
		{'expected': 
			{'name': 'pair',
			 'rank_values': [2, 14, 13, 12]
			},
		 'cards': 
			[Card(2, 'S'), Card(2, 'C'), Card(14, 'D'), Card(13, 'D'),
		 	 Card(9, 'H'), Card(11, 'D'), Card(12, 'D')]
		},
		{'expected': 
			{'name': 'pair',
			 'rank_values': [13, 12, 11, 10]
			},
		 'cards': 
			[Card(2, 'S'), Card(13, 'S'), Card(13, 'C'), Card(12, 'S'),
		 	 Card(6, 'D'), Card(10, 'S'), Card(11, 'D')]
		},
		{'expected': 
			{'name': 'high_card',
			 'rank_values': [9, 8, 7, 6, 4]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(4, 'C'), Card(6, 'H'),
		 	 Card(7, 'H'), Card(8, 'H'), Card(9, 'H')]
		},
		{'expected': 
			{'name': 'high_card',
			 'rank_values': [14, 8, 7, 6, 5]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(5, 'C'), Card(6, 'C'),
		 	 Card(7, 'C'), Card(8, 'C'), Card(14, 'S')]
		},

		{'expected': 
			{'name': 'high_card',
			 'rank_values': [12, 11, 10, 9, 5]
			},
		 'cards': 
			[Card(2, 'S'), Card(3, 'S'), Card(5, 'S'), Card(9, 'S'),
		 	 Card(10, 'C'), Card(11, 'C'), Card(12, 'C')]
		},
		{'expected': 
			{'name': 'high_card',
			 'rank_values': [14, 12, 10, 8, 6]
			},
		 'cards': 
			[Card(4, 'S'), Card(5, 'S'), Card(6, 'C'), Card(14, 'S'),
		 	 Card(12, 'S'), Card(10, 'H'), Card(8, 'H')]
		},
		{'expected': 
			{'name': 'high_card',
			 'rank_values': [14, 10, 7, 6, 4]
			},
		 'cards': 
			[Card(14, 'S'), Card(2, 'S'), Card(3, 'S'), Card(4, 'S'),
		 	 Card(6, 'H'), Card(7, 'H'), Card(10, 'H')]
		}
]

class RankTest(unittest.TestCase):
	def test_get_rank(self):
		for hand in hands:
			expected_rank = hand_rank.Rank(hand['expected']['name'], hand['expected']['rank_values'])
			actual_rank = hand_rank.get_rank(hand['cards'])
			self.assertEquals(expected_rank._to_string(), actual_rank._to_string())
