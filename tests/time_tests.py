import timeit
import csv

NUM_TESTS = 10000

def read_in_best_times():
	best_times = {}
	reader = csv.reader(open('best_times.csv', 'rb'))
	for row in reader:
		best_times[row[0]] = row[1]
	return best_times

def write_out_best_times(new_best_times):
	writer = csv.writer(open('best_times.csv', 'wb'))
	for key in sorted(new_best_times.keys()):
		writer.writerow([key, new_best_times[key]])

def time_draw():
	setup = """import classes"""
	s = """
	deck = classes.Deck()
	for _ in range(20):
		deck.draw()
	for _ in range(10):
		deck.draw(num_cards = 2)
	"""
	return timeit.timeit(s, setup, number = NUM_TESTS)

def time_simulate_hands():
	setup = """import classes; \
		import simulation"""
	s = """
		hand = classes.Hand(classes.Card(14, 'S'), classes.Card(14, 'D'))
		simulation.simulate_hands(hand, [], classes.Deck(), 10)
	"""
	return timeit.timeit(s, setup, number = NUM_TESTS / 10)

def get_random_hand():
	setup = """import hand_rank; \
		import random; \
		from classes import Hand, Card, VALUES, SUITS"""
	s = """
		hand = Hand(Card(random.choice(VALUES), random.choice(SUITS)),
			Card(random.choice(VALUES), random.choice(SUITS)))
	"""
	return setup, s

def get_random_seven_cards():
	setup = """import hand_rank; \
		import random; \
		from classes import Card, VALUES, SUITS"""
	s = """
		cards = [Card(random.choice(VALUES), random.choice(SUITS)) for _ in range(7)]
	"""
	return setup, s

def time_compare_ranks():
	setup, s = get_random_seven_cards()
	s += """
		rank1 = hand_rank.get_rank(cards)
	"""
	s += get_random_seven_cards()[1]
	s += """
		rank2 = hand_rank.get_rank(cards)
		hand_rank.Rank.compare_ranks(rank1, rank2)
	"""
	return timeit.timeit(s, setup, number = NUM_TESTS)

def time_get_rank():
	setup, s = get_random_seven_cards()
	s += """
		hand_rank.get_rank(cards)
	"""
	return timeit.timeit(s, setup, number = NUM_TESTS)

def time_get_next_seat():
	setup = """from deal import Deal; \
	from classes import Player; \
	import random; \
	deal = Deal([Player(200, 'A'), Player(200, 'B'), Player(200, 'C'), Player(200, 'D'), \
		Player(200, 'E'), Player(200, 'F'), Player(200, 'G'), Player(200, 'H')]); \
	deal.players[0].all_in = True; \
	deal.players[3].all_in = True; \
	deal.players[5].in_hand = False; \
	deal.players[6].has_acted = True; \
	deal.players[7].has_acted = True; \
	seat = 0"""
	s = """
		seat = deal.get_next_seat(seat, require_active = random.choice([True, False]))
	"""
	return timeit.timeit(s, setup, number = NUM_TESTS)

if __name__ == '__main__':
	best_times = read_in_best_times()
	new_best_times = best_times.copy()
	for test in [time_draw, time_simulate_hands, time_compare_ranks, time_get_rank, time_get_next_seat]:
		time = test()
		try:
			best_time = float(best_times[test.__name__[5:]])
		except KeyError:
			best_time = 1000.0
		print 'Time for %s: %.5f (%.5f' % (test.__name__[5:], time, 100 * (time - best_time) / best_time) + '%)'
		if time < best_time:
			new_best_times[test.__name__[5:]] = time
	write_out_best_times(new_best_times)
