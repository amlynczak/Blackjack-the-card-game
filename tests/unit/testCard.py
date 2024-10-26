import unittest
from blackjack.card import Card

class TestCard(unittest.TestCase):

    def test_card_init(self):
        card = Card('A', '♠')
        self.assertEqual(card.rank, 'A')
        self.assertEqual(card.suit, '♠')

    def test_value_cards(self):
        for rank in range(2, 10):
            card = Card(str(rank), 'U')#U is a dummy suit
            self.assertEqual(card.value(), rank)
        
        for rank in ['J', 'Q', 'K']:
            card = Card(rank, 'U')
            self.assertEqual(card.value(), 10)

        card = Card('A', 'U')
        self.assertEqual(card.value(), 11)
