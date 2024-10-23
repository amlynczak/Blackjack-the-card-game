from blackjack.deck import Deck
import unittest

class TestDeck(unittest.TestCase):

    def test_deck_init(self):
        deck = Deck()
        self.assertEqual(deck.number_of_decks, 1)
        self.assertEqual(len(deck.cards), 52)

    def test_deck_init_with_multiple_decks(self):
        number_of_decks = 4
        deck = Deck(number_of_decks)
        self.assertEqual(deck.number_of_decks, number_of_decks)
        self.assertEqual(len(deck.cards), 52 * number_of_decks)

    def test_deal_card(self):
        deck = Deck()
        card = deck.deal_card()
        self.assertEqual(len(deck.cards), 51)