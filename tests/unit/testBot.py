import unittest
import random
from blackjack.bot import Bot
from blackjack.card import Card
from blackjack.deck import Deck

class TestBot(unittest.TestCase):
    def test_bot_init(self):
        bot = Bot("Joseph Haydn")

        self.assertEqual(bot.name, "Joseph Haydn")
        self.assertEqual(len(bot.hands), 1)
        self.assertEqual(bot.money, 1000)
        self.assertEqual(bot.hand_id, 0)
        self.assertEqual(bot.insurance_bet, 0)
        self.assertFalse(bot.is_insured)
        self.assertFalse(bot.has_surrenderred)

    def test_decide_action(self):
        bot = Bot("Wolfgang Amadeus Mozart")
        deck = Deck()
        bot.add_card(deck.deal_card())
        bot.add_card(deck.deal_card())
        dealer_hand = [deck.deal_card(), deck.deal_card()]

        action = bot.decide_action(dealer_hand)

        self.assertIn(action, ['H', 'D', 'S', 'P', 'U'])

    def test_decide_final_action(self):
        bot = Bot("Frank Ocean")
        deck = Deck()
        bot.add_card(deck.deal_card())
        bot.add_card(deck.deal_card())
        dealer_hand = [deck.deal_card(), deck.deal_card()]

        action = bot.decide_final_action(dealer_hand)

        self.assertIn(action, ['hit', 'double', 'stand', 'split'])

    def test_decide_bet(self):
        bot = Bot("Belmondawg")

        bet = bot.decide_bet(10)

        self.assertIn(bet, [10, 20, 50, 100, 200, 500])
