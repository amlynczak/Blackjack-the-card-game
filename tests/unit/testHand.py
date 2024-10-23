import unittest
from blackjack.hand import Hand
from blackjack.card import Card

class TestHand(unittest.TestCase):

    def test_hand_init(self):
        name = "Test Hand"
        bet = 2137
        hand = Hand(name, bet)
        self.assertEqual(len(hand.cards), 0)
        self.assertEqual(hand.name, name)
        self.assertEqual(hand.bet, bet)
        self.assertFalse(hand.isBlackjack)

    def test_add_card(self):
        card = Card("A", "♠")
        hand = Hand("Test Hand", 69)
        hand.add_card(card)
        self.assertEqual(len(hand.cards), 1)
        self.assertEqual(hand.cards[0], card)

    def test_get_hand_value(self):
        hand1 = Hand("Test Hand 1", 11)
        hand2 = Hand("Test Hand 2", 11)

        card1 = Card("A", "♠")
        card2 = Card("K", "♠")
        card3 = Card("5", "♠")
        card4 = Card("A", "♠")

        hand1.add_card(card1)
        hand1.add_card(card4)

        self.assertEqual(hand1.get_hand_value(), 12)

        hand2.add_card(card2)
        hand2.add_card(card3)

        self.assertEqual(hand2.get_hand_value(), 15)
