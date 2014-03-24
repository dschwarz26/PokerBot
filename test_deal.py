import unittest
import utils

from classes import Card, Hand, Player
from deal import Deal

class DealTest(unittest.TestCase):
	def setUp(self):
		self.starting_chips = 1000
		Alice = Player(self.starting_chips, 'Alice')
		Bob = Player(self.starting_chips, 'Bob')
		Carl = Player(self.starting_chips, 'Carl')
		self.players = [Alice, Bob, Carl]
		
	def test_get_next_seat(self):
		deal = Deal(self.players, 1, 2, debug_level=0)
		self.assertEquals(deal.get_next_seat(0), 1)
		deal.players[1].in_hand = False
		self.assertEquals(deal.get_next_seat(0), 2)
		deal.players[2].in_hand = False
		self.assertEquals(deal.get_next_seat(0), 0)
		deal.players[1].in_hand = True
		deal.players[2].in_hand = True
		deal.players[1].has_acted = True
		self.assertEquals(deal.get_next_seat(0), 2)
		deal.players[2].has_acted = True
		self.assertEquals(deal.get_next_seat(0), 0)
		deal.players[1].has_acted = False
		deal.players[2].has_acted = False
		deal.players[1].all_in = True
		self.assertEquals(deal.get_next_seat(0), 2)
		deal.players[2].all_in = True
		self.assertEquals(deal.get_next_seat(0), 0)

	def test_set_all_other_players_active(self):
		deal = Deal(self.players, 1, 2, debug_level=0)
		self.assertEquals(deal.num_active_players_in_hand, 3)
		for i in range(len(deal.players)):
			j = (i + 1) % len(deal.players)
			k = (j + 1) % len(deal.players)
			deal.players[i].has_acted = True
			deal.set_all_other_players_active(i)
			self.assertFalse(deal.players[j].has_acted)
			self.assertFalse(deal.players[k].has_acted)
			deal.players[j].has_acted
			deal.set_all_other_players_active(i)
			self.assertFalse(deal.players[j].has_acted)
			self.assertFalse(deal.players[k].has_acted)
			deal.players[j].has_acted
			deal.players[k].has_acted
			deal.set_all_other_players_active(i)
			self.assertFalse(deal.players[j].has_acted)
			self.assertFalse(deal.players[k].has_acted)

	def set_hands(self, hands):
		for i, player in enumerate(self.players):
			player.hand = hands[i]

	def test_get_players_by_rank(self):
		deal = Deal(self.players, 1, 2, debug_level=0)
		deal.communal_cards = [Card(2, 'S'),	Card(3, 'S'), Card(5, 'H'),
			Card(7, 'D'), Card(8, 'C')]
		hands = [Hand(Card(10, 'S'), Card(10, 'H')), Hand(Card(11, 'S'), Card(11, 'H')),
			Hand(Card(12, 'S'), Card(12, 'H'))]
		self.set_hands(hands)
		self.assertEquals([player.name for player in deal.get_players_by_rank()],
			['Alice', 'Bob', 'Carl'])
		hands = [Hand(Card(11, 'S'), Card(11, 'H')), Hand(Card(10, 'S'), Card(10, 'H')),
			Hand(Card(9, 'D'), Card(9, 'H'))]
		self.set_hands(hands)
		self.assertEquals([player.name for player in deal.get_players_by_rank()],
			['Carl', 'Bob', 'Alice'])
		hands = [Hand(Card(8, 'S'), Card(10, 'H')), Hand(Card(8, 'H'), Card(14, 'H')),
			Hand(Card(8, 'D'), Card(11, 'H'))]
		self.set_hands(hands)
		self.assertEquals([player.name for player in deal.get_players_by_rank()],
			['Alice', 'Carl', 'Bob'])

	def test_update_player_with_fold(self):
		deal = Deal(self.players, 1, 2, debug_level=0)
		self.assertEquals(deal.players[deal.small_blind_seat].name, 'Bob')
		self.assertEquals(deal.players[deal.small_blind_seat].chips,
			self.starting_chips - deal.small_blind)
		big_blind_seat = deal.get_next_seat(deal.small_blind_seat)
		self.assertEquals(deal.players[big_blind_seat].chips,
			self.starting_chips - deal.big_blind)
		self.assertEquals(deal.pot, deal.small_blind + deal.big_blind)
		self.assertEquals(deal.bet, deal.big_blind)
		deal.update_player_with_action(0, ['fold'])
		self.assertEquals(deal.num_players_in_hand, len(deal.players) - 1)
		self.assertEquals(deal.pot, deal.small_blind + deal.big_blind)
		deal.update_player_with_action(1, ['fold'])
		self.assertEquals(deal.num_players_in_hand, len(deal.players) - 2)
		deal.clean_up(winning_seat=2)
		self.assertEquals(deal.players[2].chips,
			self.starting_chips + deal.small_blind)

	def test_update_player_with_all_actions(self):
		deal = Deal(self.players, 1, 2, debug_level=0)
		deal.update_player_with_action(0, ['call'])
		self.assertEquals(deal.pot, deal.small_blind + 2 * deal.big_blind)
		self.assertEquals(deal.players[0].chips, self.starting_chips - deal.big_blind)
		self.assertEquals(deal.players[0].curr_bet, deal.big_blind)
		self.assertEquals(deal.num_active_players_in_hand, 2)
		deal.update_player_with_action(1, ['call'])
		self.assertEquals(deal.pot, 3 * deal.big_blind)
		self.assertEquals(deal.players[1].chips, self.starting_chips - deal.big_blind)
		self.assertEquals(deal.players[1].curr_bet, deal.big_blind)
		self.assertEquals(deal.num_active_players_in_hand, 1)
		deal.update_player_with_action(2, ['check'])
		self.assertEquals(deal.pot, 3 * deal.big_blind)
		self.assertEquals(deal.players[2].chips, self.starting_chips - deal.big_blind)
		self.assertEquals(deal.players[2].curr_bet, deal.big_blind)
		self.assertEquals(deal.num_active_players_in_hand, 0)
		deal.clean_up_betting_round()
		self.assertEquals(deal.bet, 0)
		deal.update_player_with_action(1, ['check'])
		deal.update_player_with_action(2, ['check'])
		deal.update_player_with_action(0, ['check'])
		self.assertEquals(deal.pot, 3 * deal.big_blind)
		for player in deal.players:
			self.assertTrue(player.has_acted)
			self.assertFalse(player.all_in)
		self.assertEquals(deal.num_active_players_in_hand, 0)
		deal.clean_up_betting_round()
		deal.update_player_with_action(1, ['bet', 10])
		self.assertEquals(deal.bet, 10)
		self.assertEquals(deal.pot, 10 + 3 * deal.big_blind)
		self.assertEquals(deal.num_active_players_in_hand, len(deal.players) - 1)
		deal.update_player_with_action(2, ['call'])
		self.assertEquals(deal.players[2].chips, self.starting_chips - deal.big_blind - 10)
		self.assertEquals(deal.bet, 10)
		self.assertEquals(deal.pot, 20 + 3 * deal.big_blind)
		self.assertEquals(deal.num_active_players_in_hand, len(deal.players) - 2)
		deal.update_player_with_action(0, ['call'])
		self.assertEquals(deal.num_active_players_in_hand, 0)
		deal.clean_up_betting_round()
		self.assertEquals(deal.bet, 0)
		self.assertEquals(deal.pot, 30 + 3 * deal.big_blind)
		deal.update_player_with_action(1, ['check'])
		deal.update_player_with_action(2, ['check'])
		deal.update_player_with_action(0, ['bet', 100])
		self.assertEquals(deal.num_active_players_in_hand, len(deal.players) - 1)
		self.assertEquals(deal.pot, 130 + 3 * deal.big_blind)
		deal.update_player_with_action(1, ['call'])
		self.assertEquals(deal.num_active_players_in_hand, len(deal.players) - 2)
		self.assertEquals(deal.pot, 230 + 3 * deal.big_blind)
		deal.update_player_with_action(2, ['call'])
		self.assertEquals(deal.num_active_players_in_hand, 0)
		self.assertEquals(deal.pot, 330 + 3 * deal.big_blind)
		deal.clean_up(winning_seat = 0)
		self.assertEquals(deal.players[0].chips,
			self.starting_chips + 220 + 2 * deal.big_blind)
		self.assertEquals(deal.players[1].chips,
			self.starting_chips - 110 - deal.big_blind)
		self.assertEquals(deal.players[2].chips,
			self.starting_chips - 110 - deal.big_blind)

	def test_update_player_with_sidepot(self):
		self.players[0].chips = 10
		self.players[1].chips = 100
		self.players[2].chips = 1000
		deal = Deal(self.players, 1, 2, debug_level=0)
		deal.update_player_with_action(0, ['raise', 8])
		deal.update_player_with_action(1, ['raise', 90])
		deal.update_player_with_action(2, ['raise', 900])
		self.assertTrue(all([player.all_in for player in deal.players]))
		deal.clean_up_betting_round()
		self.assertEquals(deal.players[0].sidepot, 30)
		self.assertEquals(deal.players[1].sidepot, 210)
		self.assertEquals(deal.players[2].sidepot, 1110)

	def test_update_player_with_sidepot_2(self):
		self.players[0].chips = 10
		self.players[1].chips = 100
		self.players[2].chips = 1000
		deal = Deal(self.players, 1, 2, debug_level=0)
		deal.update_player_with_action(0, ['raise', 8])
		deal.update_player_with_action(1, ['call'])
		deal.update_player_with_action(2, ['fold'])
		deal.clean_up_betting_round()
		self.assertEquals(deal.players[0].sidepot, 22)

	def test_play_all_actions_with_sidepot(self):
		self.players[0].chips = 200
		self.players[1].chips = 400
		self.players[2].chips = 600
		deal = Deal(self.players, 1, 2, debug_level=0)
		deal.update_player_with_action(0, ['call'])
		deal.update_player_with_action(1, ['call'])
		deal.update_player_with_action(2, ['check'])
		deal.clean_up_betting_round()
		self.assertEqual(deal.pot, 6)
		self.assertFalse(any([player.all_in for player in deal.players]))
		deal.update_player_with_action(1, ['bet', 10])
		deal.update_player_with_action(2, ['call'])
		deal.update_player_with_action(0, ['raise', 188])	
		self.assertTrue(deal.players[0].all_in)
		deal.update_player_with_action(1, ['call'])
		deal.update_player_with_action(2, ['call'])
		deal.clean_up_betting_round()
		self.assertEquals(deal.players[0].sidepot, 600)
		deal.update_player_with_action(1, ['bet', 100])
		deal.update_player_with_action(2, ['raise', 100])
		deal.update_player_with_action(1, ['call'])
		self.assertTrue(deal.players[1].all_in)
		deal.clean_up_betting_round()
		self.assertEquals(deal.players[1].sidepot, 1000)
		self.assertFalse(deal.players[2].sidepot)
		deal.clean_up(players_by_rank = [
			deal.players[2],
			deal.players[1],
			deal.players[0]])
		self.assertEquals(deal.players[0].chips, 600)
		self.assertEquals(deal.players[1].chips, 400)
		self.assertEquals(deal.players[2].chips, 200)

	def test_play_all_actions_with_sidepot_2(self):
		self.players[0].chips = 1000
		self.players[1].chips = 2000
		self.players[2].chips = 3000
		self.players.append(Player(4000, 'Dave'))
		self.players.append(Player(5000, 'Elliot'))
		self.players.append(Player(6000, 'Frank'))
		self.players.append(Player(7000, 'Garret'))
		deal = Deal(self.players, 1, 2, debug_level=0)
		deal.update_player_with_action(3, ['call'])
		deal.update_player_with_action(4, ['call'])
		deal.update_player_with_action(5, ['call'])
		deal.update_player_with_action(6, ['call'])
		deal.update_player_with_action(0, ['raise', 998])
		deal.update_player_with_action(1, ['call'])
		deal.update_player_with_action(2, ['call'])
		deal.update_player_with_action(3, ['call'])
		deal.update_player_with_action(4, ['call'])
		deal.update_player_with_action(5, ['call'])
		deal.update_player_with_action(6, ['call'])
		deal.clean_up_betting_round()
		self.assertEqual(deal.players[0].sidepot, 7000)
		deal.update_player_with_action(1, ['bet', 1000])
		deal.update_player_with_action(2, ['call'])
		deal.update_player_with_action(3, ['call'])
		deal.update_player_with_action(4, ['call'])
		deal.update_player_with_action(5, ['call'])
		deal.update_player_with_action(6, ['call'])
		deal.clean_up_betting_round()
		self.assertEqual(deal.players[1].sidepot, 13000)
		deal.update_player_with_action(2, ['bet', 1000])
		deal.update_player_with_action(3, ['call'])
		deal.update_player_with_action(4, ['call'])
		deal.update_player_with_action(5, ['call'])
		deal.update_player_with_action(6, ['call'])
		deal.clean_up_betting_round()
		self.assertEqual(deal.players[2].sidepot, 18000)
		deal.update_player_with_action(3, ['bet', 1000])
		deal.update_player_with_action(4, ['raise', 1000])
		deal.update_player_with_action(5, ['call'])
		deal.update_player_with_action(6, ['fold'])
		deal.clean_up_betting_round()
		self.assertEqual(deal.players[3].sidepot, 21000)
		self.assertEqual(deal.players[4].sidepot, 23000)
		deal.clean_up(players_by_rank = [deal.players[5],
			deal.players[4], deal.players[0],
			deal.players[2], deal.players[3],
			deal.players[1]])
		self.assertEquals(deal.players[0].chips, 0)
		self.assertEquals(deal.players[1].chips, 13000)
		self.assertEquals(deal.players[2].chips, 0)	
		self.assertEquals(deal.players[3].chips, 8000)
		self.assertEquals(deal.players[4].chips, 2000)
		self.assertEquals(deal.players[5].chips, 1000)
		self.assertEquals(deal.players[6].chips, 4000)
		self.assertEquals(sum([player.chips for player in deal.players]), 28000)
