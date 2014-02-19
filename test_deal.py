import deal
from classes import Card, Hand, Player
import utils

class TestDeal:
	def __init__(self):
		Alice = Player(1000, 'Alice')
		Bob = Player(1000, 'Bob')
		Carl = Player(1000, 'Carl')
		self.default_players = [Alice, Bob, Carl]

	def set_up_test(self, players, hands=None, communal_cards=None):
		test_deal = deal.Deal(self.default_players, 1, 2, debug_level=0)
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
		communal_cards = [Card(2, 'S'),	Card(3, 'S'), Card(5, 'H'), Card(7, 'D'), Card(9, 'C')]
		hands = [Hand(Card(10, 'S'), Card(10, 'H')), Hand(Card(11, 'S'), Card(11, 'H')),
			Hand(Card(12, 'S'), Card(12, 'H'))]
		test_deal = self.set_up_test(self.default_players, hands=hands, communal_cards=communal_cards)
		assert set([player.name for player in test_deal.get_winners()])  == set(['Carl'])
		hands = [Hand(Card(10, 'S'), Card(10, 'H')), Hand(Card(11, 'S'), Card(11, 'H')),
			Hand(Card(11, 'D'), Card(11, 'H'))]
		test_deal = self.set_up_test(self.default_players, hands=hands, communal_cards=communal_cards)
		assert set([player.name for player in test_deal.get_winners()]) == set(['Bob', 'Carl'])
		hands = [Hand(Card(11, 'S'), Card(11, 'H')), Hand(Card(11, 'S'), Card(11, 'H')),
			Hand(Card(11, 'D'), Card(11, 'H'))]
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
