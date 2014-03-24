from classes import Player
import random

#FoldPlayer folds at the first opportunity.
class FoldPlayer(Player):
	def get_action(self, deal):
		return ['fold']
#AllInPlayer goes all in at the first opportunity.
class AllInPlayer(Player):
	def get_action(self, deal):
		return ['raise', self.chips - deal.bet + self.curr_bet]	

#CallPlayer always calls, or checks if there is no bet.
class CallPlayer(Player):
	def get_action(self, deal):
		if deal.bet == 0:
			return ['check']
		return ['call']
	
#RandomPlayer picks a random valid action at each bet. If that action
#is a bet or raise, RandomPlayer picks a random valid bet/raise amount.
class RandomPlayer(Player):
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
