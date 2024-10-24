import unittest
from blackjack.game import BlackjackGame

class TestBlackjackGame(unittest.TestCase):
    def test_blackjack_game_init(self):
        game = BlackjackGame(4, 5, 40)

        self.assertEqual(game.deck.cards.__len__(), 52 * 4)

        self.assertEqual(game.standard_bet, 40)

        self.assertEqual(game.main_player.name, "Player")
        self.assertEqual(game.main_player.money, 1000)
        self.assertEqual(game.main_player.hand_id, 0)
        self.assertEqual(game.main_player.insurance_bet, 0)
        self.assertFalse(game.main_player.isInsured)
        self.assertFalse(game.main_player.has_surrenderred)

        self.assertEqual(game.bot_players.__len__(), 4)

        self.assertEqual(game.dealer.name, "Dealer")

    def test_start_new_round(self):
        game = BlackjackGame()
        game.start_new_round()

        self.assertEqual(game.main_player.hands[0].cards.__len__(), 2)
        self.assertEqual(game.dealer.hand.__len__(), 2)
