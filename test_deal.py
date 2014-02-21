import deal
from classes import Card, Hand, Player
import utils

class TestDeal:
	def __init__(self):
		self.starting_chips = 1000

	def set_up_test(self, hands=None, communal_cards=None):
		Alice = Player(self.starting_chips, 'Alice')
		Bob = Player(self.starting_chips, 'Bob')
		Carl = Player(self.starting_chips, 'Carl')
		players = [Alice, Bob, Carl]
		self.num_players = 3
		test_deal = deal.Deal(players, 1, 2, debug_level=0)
		if hands:
			for i, player in enumerate(test_deal.players):
				player.hand = hands[i]
		if communal_cards:
			test_deal.communal_cards = communal_cards
		return test_deal
	
	def test_get_next_active_seat(self):
		test_deal = self.set_up_test()
		assert test_deal.get_next_active_seat(0) == 1
		test_deal.players[1].in_hand = False
		assert test_deal.get_next_active_seat(0) == 2
		test_deal.players[2].in_hand = False
		assert test_deal.get_next_active_seat(0) == 0
		
		test_deal = self.set_up_test()
		test_deal.players[1].has_acted = True
		assert test_deal.get_next_active_seat(0) == 2
		test_deal.players[2].has_acted = True
		assert test_deal.get_next_active_seat(0) == 0

		test_deal = self.set_up_test()
		test_deal.players[1].all_in = True
		assert test_deal.get_next_active_seat(0) == 2
		test_deal.players[2].all_in = True
		assert test_deal.get_next_active_seat(0) == 0

	def test_set_all_other_players_active(self):
		test_deal = self.set_up_test()
		assert test_deal.num_active_players_in_hand == 3
		for i in range(len(test_deal.players)):
			j = (i + 1) % len(test_deal.players)
			k = (j + 1) % len(test_deal.players)
			test_deal.players[i].has_acted = True
			test_deal.set_all_other_players_active(i)
			assert not test_deal.players[j].has_acted
			assert not test_deal.players[k].has_acted
			test_deal.players[j].has_acted
			test_deal.set_all_other_players_active(i)
			assert not test_deal.players[j].has_acted
			assert not test_deal.players[k].has_acted
			test_deal.players[j].has_acted
			test_deal.players[k].has_acted
			test_deal.set_all_other_players_active(i)
			assert not test_deal.players[j].has_acted
			assert not test_deal.players[k].has_acted

	def test_get_winners(self):
		communal_cards = [Card(2, 'S'),	Card(3, 'S'), Card(5, 'H'), Card(7, 'D'), Card(9, 'C')]
		hands = [Hand(Card(10, 'S'), Card(10, 'H')), Hand(Card(11, 'S'), Card(11, 'H')),
			Hand(Card(12, 'S'), Card(12, 'H'))]
		test_deal = self.set_up_test(hands=hands, communal_cards=communal_cards)
		assert set([player.name for player in test_deal.get_winners()])  == set(['Carl'])
		hands = [Hand(Card(10, 'S'), Card(10, 'H')), Hand(Card(11, 'S'), Card(11, 'H')),
			Hand(Card(11, 'D'), Card(11, 'H'))]
		test_deal = self.set_up_test(hands=hands, communal_cards=communal_cards)
		assert set([player.name for player in test_deal.get_winners()]) == set(['Bob', 'Carl'])
		hands = [Hand(Card(11, 'S'), Card(11, 'H')), Hand(Card(11, 'S'), Card(11, 'H')),
			Hand(Card(11, 'D'), Card(11, 'H'))]
		test_deal = self.set_up_test(hands=hands, communal_cards=communal_cards)
		assert set([player.name for player in test_deal.get_winners()]) == set(['Alice', 'Bob', 'Carl'])
		
	def test_update_player_with_action(self):
		test_deal = self.set_up_test()
		assert test_deal.players[test_deal.small_blind_seat].name == 'Bob'
		test_deal.initiate_round()
		assert test_deal.players[test_deal.small_blind_seat].chips == self.starting_chips - test_deal.small_blind
		big_blind_seat = test_deal.get_next_active_seat(test_deal.small_blind_seat)
		assert test_deal.players[big_blind_seat].chips == self.starting_chips - test_deal.big_blind
		assert test_deal.pot == test_deal.small_blind + test_deal.big_blind
		assert test_deal.bet == test_deal.big_blind
		test_deal.update_player_with_action(0, ['fold'])
		assert test_deal.num_players_in_hand == len(test_deal.players) - 1
		assert test_deal.pot == test_deal.small_blind + test_deal.big_blind
		test_deal.update_player_with_action(1, ['fold'])
		assert test_deal.num_players_in_hand == len(test_deal.players) - 2
		test_deal.clean_up(winning_seat=2)
		assert test_deal.players[2].chips == self.starting_chips + test_deal.small_blind

		test_deal = self.set_up_test()
		test_deal.initiate_round()
		test_deal.update_player_with_action(0, ['call'])
		assert test_deal.pot == test_deal.small_blind + 2 * test_deal.big_blind
		assert test_deal.players[0].chips == self.starting_chips - test_deal.big_blind
		assert test_deal.players[0].curr_bet == test_deal.big_blind
		assert test_deal.num_active_players_in_hand == 2
		test_deal.update_player_with_action(1, ['call'])
		assert test_deal.pot == 3 * test_deal.big_blind
		assert test_deal.players[1].chips == self.starting_chips - test_deal.big_blind
		assert test_deal.players[1].curr_bet == test_deal.big_blind
		assert test_deal.num_active_players_in_hand == 1
		test_deal.update_player_with_action(2, ['check'])
		assert test_deal.pot == 3 * test_deal.big_blind
		assert test_deal.players[2].chips == self.starting_chips - test_deal.big_blind
		assert test_deal.players[2].curr_bet == test_deal.big_blind
		assert test_deal.num_active_players_in_hand == 0
		test_deal.clean_up_betting_round()
		assert test_deal.bet == 0
		test_deal.update_player_with_action(1, ['check'])
		test_deal.update_player_with_action(2, ['check'])
		test_deal.update_player_with_action(0, ['check'])
		assert test_deal.pot == 3 * test_deal.big_blind
		for player in test_deal.players:
			assert player.has_acted
			assert not player.all_in
		assert test_deal.num_active_players_in_hand == 0
		test_deal.clean_up_betting_round()
		test_deal.update_player_with_action(1, ['bet', 10])
		assert test_deal.bet == 10
		assert test_deal.pot == 10 + 3 * test_deal.big_blind
		assert test_deal.num_active_players_in_hand == len(test_deal.players) - 1
		test_deal.update_player_with_action(2, ['call'])
		assert test_deal.players[2].chips == self.starting_chips - test_deal.big_blind - 10
		assert test_deal.bet == 10
		assert test_deal.pot == 20 + 3 * test_deal.big_blind
		assert test_deal.num_active_players_in_hand == len(test_deal.players) - 2
		test_deal.update_player_with_action(0, ['call'])
		assert test_deal.num_active_players_in_hand == 0
		test_deal.clean_up_betting_round()
		assert test_deal.bet == 0
		assert test_deal.pot == 30 + 3 * test_deal.big_blind
		test_deal.update_player_with_action(1, ['check'])
		test_deal.update_player_with_action(2, ['check'])
		test_deal.update_player_with_action(0, ['bet', 100])
		assert test_deal.num_active_players_in_hand == len(test_deal.players) - 1
		assert test_deal.pot == 130 + 3 * test_deal.big_blind
		test_deal.update_player_with_action(1, ['call'])
		assert test_deal.num_active_players_in_hand == len(test_deal.players) - 2
		assert test_deal.pot == 230 + 3 * test_deal.big_blind
		test_deal.update_player_with_action(2, ['call'])
		assert test_deal.num_active_players_in_hand == 0
		assert test_deal.pot == 330 + 3 * test_deal.big_blind
		test_deal.clean_up(winning_seat = 0)
		assert test_deal.players[0].chips == self.starting_chips + 220 + 2 * test_deal.big_blind
		assert test_deal.players[1].chips == self.starting_chips - 110 - test_deal.big_blind
		assert test_deal.players[2].chips == self.starting_chips - 110 - test_deal.big_blind
		
if __name__ == '__main__':
	testDeal = TestDeal()
	testDeal.test_get_next_active_seat()
	testDeal.test_get_winners()
	testDeal.test_update_player_with_action()
