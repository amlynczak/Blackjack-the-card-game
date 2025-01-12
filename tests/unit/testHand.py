import unittest
import random
from blackjack.hand import Hand
from blackjack.card import Card

class TestHand(unittest.TestCase):
    def test_add_card(self):
        card = Card("A", "♠")
        hand = Hand("Pablo", 69)
        hand.add_card(card)
        self.assertEqual(len(hand.cards), 1)
        self.assertEqual(hand.cards[0], card)

    def test_get_hand_value_no_aces_with_changing_value(self):
        hand = Hand("Frank Ocean", 11)

        random_number_1 = random.randint(2, 10)
        random_rank = random.randint(2, 14)
        if random_rank == 11:
            random_rank = 'J'
        elif random_rank == 12:
            random_rank = 'Q'
        elif random_rank == 13:
            random_rank = 'K'
        elif random_rank == 14:
            random_rank = 'A'

        card1 = Card(str(random_number_1), "unknown")
        card2 = Card(str(random_rank), "Donda")

        hand.add_card(card1)
        hand.add_card(card2)

        self.assertEqual(hand.get_hand_value(), (card1.value()+card2.value()))

    def test_get_hand_value_aces_with_changing_value(self):
        hand = Hand("Joseph Haydn", 420)

        card1 = Card("A", "Black")
        card2 = Card("6", "Red")
        card3 = Card("A", "Blue")
        card4 = Card("10", "Yellow")

        hand.add_card(card1)
        hand.add_card(card2)
        self.assertEqual(hand.get_hand_value(), 17)

        hand.add_card(card3)
        self.assertEqual(hand.get_hand_value(), 18)

        hand.add_card(card4)
        self.assertEqual(hand.get_hand_value(), 18)

    def test_hit(self):
        hand = Hand("Karol Wojtyla", 47)
        card1 = Card("A", "Pik")
        card2 = Card("4", "Karo")
        hand.add_card(card1)
        hand.add_card(card2)

        card3 = Card("10", "Kier")
        result = hand.hit(card3)

        self.assertEqual(len(hand.cards), 3)
        self.assertEqual(hand.get_hand_value(), 15)
        self.assertTrue(result)

        result = hand.hit(card3)

        self.assertEqual(len(hand.cards), 4)
        self.assertEqual(hand.get_hand_value(), 25)
        self.assertFalse(result)

    def test_double_down(self):
        hand = Hand("Adam Małysz", 10)
        card = Card("A", "♠")
        hand.add_card(card)
        hand.add_card(card)

        result = hand.double_down(card)

        self.assertEqual(len(hand.cards), 3)
        self.assertEqual(hand.bet, 20)
        self.assertFalse(result)
