import unittest

from tests.test_hand_rank import *
from tests.test_deal import *
from tests.test_classes import *

if __name__ == '__main__':
	suite = unittest.TestSuite([
		unittest.TestLoader().loadTestsFromTestCase(DeckTest),
		unittest.TestLoader().loadTestsFromTestCase(RankTest),
		unittest.TestLoader().loadTestsFromTestCase(DealTest)
	])
	unittest.TextTestRunner(verbosity=2).run(suite)
