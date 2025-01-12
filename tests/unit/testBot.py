import unittest
from blackjack.bot import Bot
from blackjack.deck import Deck

class TestBot(unittest.TestCase):
    def test_decide_action(self):
        bot = Bot("Domino")
        deck = Deck()
        bot.add_card(deck.deal_card())
        bot.add_card(deck.deal_card())
        dealer_hand = [deck.deal_card(), deck.deal_card()]

        action = bot.decide_action(dealer_hand)

        self.assertIn(action, ['H', 'D', 'S', 'P', 'U'])

    def test_decide_final_action(self):
        bot = Bot("Andrzej Lika")
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
