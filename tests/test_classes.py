from game import classes
import unittest

class DeckTest(unittest.TestCase):
	def test_draw(self):
		deck = classes.Deck()
		cards = deck.draw()
		self.assertEquals(len(cards), 1)
		deck.shuffle()
		cards = deck.draw(10)
		self.assertEquals(len(cards), 10)
		deck.shuffle()
		self.assertEquals([], deck.draw(100))
