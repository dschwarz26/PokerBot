import deal
import unittest
import utils

from classes import Card, Hand, Player

class DealTest(unittest.TestCase):
	def setUp(self):
		self.starting_chips = 1000
		Alice = Player(self.starting_chips, 'Alice')
		Bob = Player(self.starting_chips, 'Bob')
		Carl = Player(self.starting_chips, 'Carl')
		players = [Alice, Bob, Carl]
		self.num_players = 3
		self.test_deal = deal.Deal(players, 1, 2, debug_level=0)
	
	def test_get_next_seat(self):
		self.assertEquals(self.test_deal.get_next_seat(0), 1)
		self.test_deal.players[1].in_hand = False
		self.assertEquals(self.test_deal.get_next_seat(0), 2)
		self.test_deal.players[2].in_hand = False
		self.assertEquals(self.test_deal.get_next_seat(0), 0)
		self.test_deal.players[1].in_hand = True
		self.test_deal.players[2].in_hand = True
		self.test_deal.players[1].has_acted = True
		self.assertEquals(self.test_deal.get_next_seat(0), 2)
		self.test_deal.players[2].has_acted = True
		self.assertEquals(self.test_deal.get_next_seat(0), 0)
		self.test_deal.players[1].has_acted = False
		self.test_deal.players[2].has_acted = False
		self.test_deal.players[1].all_in = True
		self.assertEquals(self.test_deal.get_next_seat(0), 2)
		self.test_deal.players[2].all_in = True
		self.assertEquals(self.test_deal.get_next_seat(0), 0)

	def test_set_all_other_players_active(self):
		self.assertEquals(self.test_deal.num_active_players_in_hand, 3)
		for i in range(len(self.test_deal.players)):
			j = (i + 1) % len(self.test_deal.players)
			k = (j + 1) % len(self.test_deal.players)
			self.test_deal.players[i].has_acted = True
			self.test_deal.set_all_other_players_active(i)
			self.assertFalse(self.test_deal.players[j].has_acted)
			self.assertFalse(self.test_deal.players[k].has_acted)
			self.test_deal.players[j].has_acted
			self.test_deal.set_all_other_players_active(i)
			self.assertFalse(self.test_deal.players[j].has_acted)
			self.assertFalse(self.test_deal.players[k].has_acted)
			self.test_deal.players[j].has_acted
			self.test_deal.players[k].has_acted
			self.test_deal.set_all_other_players_active(i)
			self.assertFalse(self.test_deal.players[j].has_acted)
			self.assertFalse(self.test_deal.players[k].has_acted)

	def set_hands(self, hands):
		for i, player in enumerate(self.test_deal.players):
			player.hand = hands[i]

	def test_get_players_by_rank(self):
		self.test_deal.communal_cards = [Card(2, 'S'),	Card(3, 'S'), Card(5, 'H'),
			Card(7, 'D'), Card(8, 'C')]
		hands = [Hand(Card(10, 'S'), Card(10, 'H')), Hand(Card(11, 'S'), Card(11, 'H')),
			Hand(Card(12, 'S'), Card(12, 'H'))]
		self.set_hands(hands)
		self.assertEquals([player.name for player in self.test_deal.get_players_by_rank()],
			['Alice', 'Bob', 'Carl'])
		hands = [Hand(Card(11, 'S'), Card(11, 'H')), Hand(Card(10, 'S'), Card(10, 'H')),
			Hand(Card(9, 'D'), Card(9, 'H'))]
		self.set_hands(hands)
		self.assertEquals([player.name for player in self.test_deal.get_players_by_rank()],
			['Carl', 'Bob', 'Alice'])
		hands = [Hand(Card(8, 'S'), Card(10, 'H')), Hand(Card(8, 'H'), Card(14, 'H')),
			Hand(Card(8, 'D'), Card(11, 'H'))]
		self.set_hands(hands)
		self.assertEquals([player.name for player in self.test_deal.get_players_by_rank()],
			['Alice', 'Carl', 'Bob'])

	def test_update_player_with_fold(self):
		self.assertEquals(self.test_deal.players[self.test_deal.small_blind_seat].name, 'Bob')
		self.test_deal.initiate_round()
		self.assertEquals(self.test_deal.players[self.test_deal.small_blind_seat].chips,
			self.starting_chips - self.test_deal.small_blind)
		big_blind_seat = self.test_deal.get_next_seat(self.test_deal.small_blind_seat)
		self.assertEquals(self.test_deal.players[big_blind_seat].chips,
			self.starting_chips - self.test_deal.big_blind)
		self.assertEquals(self.test_deal.pot, self.test_deal.small_blind + self.test_deal.big_blind)
		self.assertEquals(self.test_deal.bet, self.test_deal.big_blind)
		self.test_deal.update_player_with_action(0, ['fold'])
		self.assertEquals(self.test_deal.num_players_in_hand, len(self.test_deal.players) - 1)
		self.assertEquals(self.test_deal.pot, self.test_deal.small_blind + self.test_deal.big_blind)
		self.test_deal.update_player_with_action(1, ['fold'])
		self.assertEquals(self.test_deal.num_players_in_hand, len(self.test_deal.players) - 2)
		self.test_deal.clean_up(winning_seat=2)
		self.assertEquals(self.test_deal.players[2].chips,
			self.starting_chips + self.test_deal.small_blind)

	def test_update_player_with_all_actions(self):
		self.test_deal.initiate_round()
		self.test_deal.update_player_with_action(0, ['call'])
		self.assertEquals(self.test_deal.pot, self.test_deal.small_blind + 2 * self.test_deal.big_blind)
		self.assertEquals(self.test_deal.players[0].chips, self.starting_chips - self.test_deal.big_blind)
		self.assertEquals(self.test_deal.players[0].curr_bet, self.test_deal.big_blind)
		self.assertEquals(self.test_deal.num_active_players_in_hand, 2)
		self.test_deal.update_player_with_action(1, ['call'])
		self.assertEquals(self.test_deal.pot, 3 * self.test_deal.big_blind)
		self.assertEquals(self.test_deal.players[1].chips, self.starting_chips - self.test_deal.big_blind)
		self.assertEquals(self.test_deal.players[1].curr_bet, self.test_deal.big_blind)
		self.assertEquals(self.test_deal.num_active_players_in_hand, 1)
		self.test_deal.update_player_with_action(2, ['check'])
		self.assertEquals(self.test_deal.pot, 3 * self.test_deal.big_blind)
		self.assertEquals(self.test_deal.players[2].chips, self.starting_chips - self.test_deal.big_blind)
		self.assertEquals(self.test_deal.players[2].curr_bet, self.test_deal.big_blind)
		self.assertEquals(self.test_deal.num_active_players_in_hand, 0)
		self.test_deal.clean_up_betting_round()
		self.assertEquals(self.test_deal.bet, 0)
		self.test_deal.update_player_with_action(1, ['check'])
		self.test_deal.update_player_with_action(2, ['check'])
		self.test_deal.update_player_with_action(0, ['check'])
		self.assertEquals(self.test_deal.pot, 3 * self.test_deal.big_blind)
		for player in self.test_deal.players:
			self.assertTrue(player.has_acted)
			self.assertFalse(player.all_in)
		self.assertEquals(self.test_deal.num_active_players_in_hand, 0)
		self.test_deal.clean_up_betting_round()
		self.test_deal.update_player_with_action(1, ['bet', 10])
		self.assertEquals(self.test_deal.bet, 10)
		self.assertEquals(self.test_deal.pot, 10 + 3 * self.test_deal.big_blind)
		self.assertEquals(self.test_deal.num_active_players_in_hand, len(self.test_deal.players) - 1)
		self.test_deal.update_player_with_action(2, ['call'])
		self.assertEquals(self.test_deal.players[2].chips, self.starting_chips - self.test_deal.big_blind - 10)
		self.assertEquals(self.test_deal.bet, 10)
		self.assertEquals(self.test_deal.pot, 20 + 3 * self.test_deal.big_blind)
		self.assertEquals(self.test_deal.num_active_players_in_hand, len(self.test_deal.players) - 2)
		self.test_deal.update_player_with_action(0, ['call'])
		self.assertEquals(self.test_deal.num_active_players_in_hand, 0)
		self.test_deal.clean_up_betting_round()
		self.assertEquals(self.test_deal.bet, 0)
		self.assertEquals(self.test_deal.pot, 30 + 3 * self.test_deal.big_blind)
		self.test_deal.update_player_with_action(1, ['check'])
		self.test_deal.update_player_with_action(2, ['check'])
		self.test_deal.update_player_with_action(0, ['bet', 100])
		self.assertEquals(self.test_deal.num_active_players_in_hand, len(self.test_deal.players) - 1)
		self.assertEquals(self.test_deal.pot, 130 + 3 * self.test_deal.big_blind)
		self.test_deal.update_player_with_action(1, ['call'])
		self.assertEquals(self.test_deal.num_active_players_in_hand, len(self.test_deal.players) - 2)
		self.assertEquals(self.test_deal.pot, 230 + 3 * self.test_deal.big_blind)
		self.test_deal.update_player_with_action(2, ['call'])
		self.assertEquals(self.test_deal.num_active_players_in_hand, 0)
		self.assertEquals(self.test_deal.pot, 330 + 3 * self.test_deal.big_blind)
		self.test_deal.clean_up(winning_seat = 0)
		self.assertEquals(self.test_deal.players[0].chips,
			self.starting_chips + 220 + 2 * self.test_deal.big_blind)
		self.assertEquals(self.test_deal.players[1].chips,
			self.starting_chips - 110 - self.test_deal.big_blind)
		self.assertEquals(self.test_deal.players[2].chips,
			self.starting_chips - 110 - self.test_deal.big_blind)

	def test_update_player_with_sidepot(self):
		self.test_deal.players[0].chips = 10
		self.test_deal.players[1].chips = 100
		self.test_deal.players[2].chips = 1000
		self.test_deal.initiate_round()
		self.test_deal.update_player_with_action(0, ['raise', 8])
		self.test_deal.update_player_with_action(1, ['raise', 90])
		self.test_deal.update_player_with_action(2, ['raise', 900])
		self.assertTrue(all([player.all_in for player in self.test_deal.players]))
		self.test_deal.play_all_actions(0)
		self.assertEquals(self.test_deal.players[0].sidepot, 30)
		self.assertEquals(self.test_deal.players[1].sidepot, 210)
		self.assertEquals(self.test_deal.players[2].sidepot, 1110)
