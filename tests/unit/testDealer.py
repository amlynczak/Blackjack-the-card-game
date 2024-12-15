import unittest
from unittest.mock import Mock
import random
import pygame

from blackjack.dealer import Dealer
from blackjack.card import Card
from blackjack.deck import Deck
from blackjack.player import Player
from blackjack.bot import Bot

class TestDealer(unittest.TestCase):

    def test_dealer_init(self):
        dealer = Dealer()
        self.assertEqual(dealer.name, "Dealer")
        self.assertEqual(len(dealer.hand), 0)

    def test_add_card(self):
        dealer = Dealer()
        card = Card("A", "rsenal")
        dealer.add_card(card)
        self.assertEqual(dealer.hand.__len__(), 1)

    def test_get_hand_value_no_aces_with_changing_value(self):
        dealer = Dealer()

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

        card1 = Card(str(random_number_1), "spades")
        card2 = Card(str(random_rank), "hearts")

        dealer.add_card(card1)
        dealer.add_card(card2)

        self.assertEqual(dealer.get_hand_value(), (card1.value()+card2.value()))

    def test_get_hand_value_aces_with_changing_value(self):
        dealer = Dealer()

        card1 = Card("A", "spades")
        card2 = Card("6", "hearts")
        card3 = Card("A", "diamonds")
        card4 = Card("10", "clubs")

        dealer.add_card(card1)
        dealer.add_card(card2)
        self.assertEqual(dealer.get_hand_value(), 17)

        dealer.add_card(card3)
        self.assertEqual(dealer.get_hand_value(), 18)

        dealer.add_card(card4)
        self.assertEqual(dealer.get_hand_value(), 18)

    def test_reset_hand(self):
        dealer = Dealer()
        deck = Deck()
        dealer.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())

        dealer.reset_hand()

        self.assertEqual(len(dealer.hand), 0)

    def test_should_hit(self):
        dealer = Dealer()
        card = Card("8", "osiem")
        dealer.add_card(card)
        dealer.add_card(card)

        self.assertTrue(dealer.should_hit())

        dealer.add_card(card)

        self.assertFalse(dealer.should_hit())