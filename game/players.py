from classes import Player
import random
import simulation

#FoldPlayer folds at the first opportunity.
class FoldPlayer(Player):
	__name__ = 'FoldPlayer'

	def get_action(self, deal):
		return ['fold']

#AllInPlayer goes all in at the first opportunity.
class AllInPlayer(Player):
	__name__ = 'AllInPlayer'

	def get_action(self, deal):
		return ['raise', self.chips - deal.bet + self.curr_bet]

#CallPlayer always calls, or checks if there is no bet.
class CallPlayer(Player):
	__name__ = 'CallPlayer'

	def get_action(self, deal):
		if deal.bet == 0:
			return ['check']
		return ['call']
	
#RandomPlayer picks a random valid action at each bet. If that action
#is a bet or raise, RandomPlayer picks a random valid bet/raise amount.
class RandomPlayer(Player):
	__name__ = 'RandomPlayer'

	def get_random_raise_increase(self, deal):
                 amount_to_call = deal.bet - self.curr_bet
                 max_raise_increase = self.chips - amount_to_call
                 min_raise_increase = deal.curr_raise if deal.curr_raise else deal.bet
                 raise_increase = (random.randint(min_raise_increase, max_raise_increase)
                         if min_raise_increase < max_raise_increase
                         else max_raise_increase)
                 return raise_increase
 
        def get_random_bet(self, deal):
                 min_bet = min(self.chips, deal.big_blind)
                 max_bet = self.chips
                 bet = random.randint(min_bet, max_bet)
                 return bet

	def get_action(self, deal):
		if deal.bet == 0:
			action = ['check', 'bet'][random.randint(0, 1)]
			if action == 'check':
				return ['check']
	                else:
	                        return ['bet', self.get_random_bet(deal)]
	        if self.curr_bet < deal.bet:
	                #If calling would put the player all in, they must either call or fold.
	                if self.chips <= deal.bet - self.curr_bet:
	                        return [['call', 'fold'][random.randint(0, 1)]]
	                else:
	                        action = ['call', 'raise', 'fold'][random.randint(0, 2)]
                        if action in ['call', 'fold']:
                                return [action]
                        else:
                                return ['raise', self.get_random_raise_increase(deal)]
 
                #Remaing case is that it's preflop and the big blind has option.
                action = ['check', 'raise'][random.randint(0, 1)]
                if action == 'check':
                        return ['check']
                else:
                        return ['raise', self.get_random_raise_increase(deal)]

#TAGPlayer goes all in when holding a pair of Js or higher or AK, and otherwise folds.
class TAGPlayer(Player):
	__name__ = 'TAGPlayer'
	pairs_to_play = [11, 12, 13, 14]
	high_cards_to_play = [13, 14]
	def get_action(self, deal):
		if (self.hand.card_one.value in self.pairs_to_play and
			self.hand.card_two.value == self.hand.card_one.value) or (
			self.hand.card_one.value in self.high_cards_to_play and
			self.hand.card_two.value in self.high_cards_to_play):
			return ['raise', self.chips - deal.bet + self.curr_bet]
		else:
			return ['fold']

class LooseTAGPlayer(TAGPlayer):
	__name__ = 'LooseTAGPlayer'
	pairs_to_play = [8, 9, 10, 11, 12, 13, 14]
	high_cards_to_play = [11, 12, 13, 14]

class TightTAGPlayer(TAGPlayer):
	__name__ = 'TightTAGPlayer'
	pairs_to_play = [13, 14]
	high_cards_to_play = [13, 14]

#SmallSimulationPlayer does small simulations of hand outcomes to determine actions.
class SimulationPlayer(Player):
	__name__ = 'SimulationPlayer'
	simulation_depth = 50
	safety_margin = 0.15

	def get_action(self, deal):
		#If the hand is preflop, call anything.
		if len(deal.communal_cards) == 0:
			return ['call']
		
		#Otherwise, go all in if either the simulation is favorable or the player is pot committed.
		winning_hands = simulation.simulate_hands(
			self.hand, deal.communal_cards, deal.deck, self.simulation_depth)
		chance_to_win = float(winning_hands) / self.simulation_depth
		pot_odds = float(self.chips) / (deal.pot + 2 * self.chips)
		if chance_to_win > pot_odds + self.safety_margin:
			return ['raise', self.chips - deal.bet + self.curr_bet]	
		else:
			return ['fold']

class SmallSimulationPlayer(SimulationPlayer):
	__name__ = 'SmallSimulationPlayer'
	simulation_depth = 20

class SmallTAGSimulationPlayer(SimulationPlayer):
	__name__ = 'SmallTAGSimulationPlayer'
	simulation_depth = 20
	safety_margin = 0.3

class SmallLAGSimulationPlayer(SimulationPlayer):
	__name__ = 'SmallLAGSimulationPlayer'
	simulation_depth = 20
	safety_margin = 0.0

class LargeSimulationPlayer(SimulationPlayer):
	__name__ = 'LargeSimulationPlayer'
	simulation_depth = 100

class LargeTAGSimulationPlayer(SimulationPlayer):
	__name__ = 'LargeTAGSimulationPlayer'
	simulation_depth = 100
	safety_margin = 0.3

class LargeLAGSimulationPlayer(SimulationPlayer):
	__name__ = 'LargeLAGSimulationPlayer'
	simulation_dept = 100
	safety_margin = 0.0
