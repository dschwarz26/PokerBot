import deal
import classes
import utils

class TestDeal:
	def __init__(self):
		Alice = classes.Player(1000, 'Alice')
		Bob = classes.Player(1000, 'Bob')
		Carl = classes.Player(1000, 'Carl')
		self.default_players = [Alice, Bob, Carl]

	def set_up_test(self, players, hands=None, communal_cards=None):
		test_deal = deal.Deal(self.default_players, 1, 2, debug_level=1)
		if hands:
			for i, player in enumerate(test_deal.players):
				player.hand = hands[i]
		if communal_cards:
			test_deal.communal_cards = communal_cards
		return test_deal
	
	def test_get_next_active_seat(self):
		test_deal = self.set_up_test(self.default_players)
		assert test_deal.get_next_active_seat(0) == 1
		test_deal.players[1].in_hand = False
		assert test_deal.get_next_active_seat(0) == 2
		test_deal.players[2].in_hand = False
		assert test_deal.get_next_active_seat(0) == 0

	def test_get_winners(self):
		communal_cards = [classes.Card(2, classes.SUITS[0]),
				  classes.Card(3, classes.SUITS[0]),
				  classes.Card(5, classes.SUITS[1]),
				  classes.Card(7, classes.SUITS[2]),
				  classes.Card(9, classes.SUITS[3])]
		hands = [classes.Hand(classes.Card(10, classes.SUITS[0]), classes.Card(10, classes.SUITS[1])),
			classes.Hand(classes.Card(11, classes.SUITS[0]), classes.Card(11, classes.SUITS[1])),
			classes.Hand(classes.Card(12, classes.SUITS[0]), classes.Card(12, classes.SUITS[1]))]
		test_deal = self.set_up_test(self.default_players, hands=hands, communal_cards=communal_cards)
		assert set([player.name for player in test_deal.get_winners()])  == set(['Carl'])
		hands = [classes.Hand(classes.Card(10, classes.SUITS[0]), classes.Card(10, classes.SUITS[1])),
			classes.Hand(classes.Card(11, classes.SUITS[0]), classes.Card(11, classes.SUITS[1])),
			classes.Hand(classes.Card(11, classes.SUITS[2]), classes.Card(11, classes.SUITS[1]))]
		test_deal = self.set_up_test(self.default_players, hands=hands, communal_cards=communal_cards)
		assert set([player.name for player in test_deal.get_winners()]) == set(['Bob', 'Carl'])
		hands = [classes.Hand(classes.Card(11, classes.SUITS[0]), classes.Card(11, classes.SUITS[1])),
			classes.Hand(classes.Card(11, classes.SUITS[0]), classes.Card(11, classes.SUITS[1])),
			classes.Hand(classes.Card(11, classes.SUITS[2]), classes.Card(11, classes.SUITS[1]))]
		test_deal = self.set_up_test(self.default_players, hands=hands, communal_cards=communal_cards)
		assert set([player.name for player in test_deal.get_winners()]) == set(['Alice', 'Bob', 'Carl'])
		
	def test_update_player_with_action(self):
		#TO DO
		pass

if __name__ == '__main__':
	testDeal = TestDeal()
	testDeal.test_get_next_active_seat()
	testDeal.test_get_winners()
	testDeal.test_update_player_with_action()
