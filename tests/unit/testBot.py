import unittest
import random
from blackjack.bot import Bot
from blackjack.card import Card
from blackjack.deck import Deck

class TestBot(unittest.TestCase):
    def test_bot_init(self):
        bot = Bot("Bot")

        self.assertEqual(bot.name, "Bot")
        self.assertEqual(len(bot.hands), 1)
        self.assertEqual(bot.money, 1000)
        self.assertEqual(bot.hand_id, 0)
        self.assertEqual(bot.insurance_bet, 0)
        self.assertFalse(bot.isInsured)
        self.assertFalse(bot.has_surrenderred)

    def test_decide_action(self):
        bot = Bot("Bot")
        deck = Deck()
        bot.add_card(deck.deal_card())
        bot.add_card(deck.deal_card())
        dealer_hand = [deck.deal_card(), deck.deal_card()]

        action = bot.decide_action(dealer_hand)

        self.assertIn(action, ['hit', 'double', 'split', 'stand'])