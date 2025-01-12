import unittest
from blackjack.player import Player
from blackjack.deck import Deck
from blackjack.card import Card
from blackjack.dealer import Dealer

class TestPlayer(unittest.TestCase):
    def test_player_add_card(self):
        player = Player("Kanye West")
        player.add_card(Card("K", "spades"))

        self.assertEqual(len(player.hands[player.hand_id].cards), 1)
        self.assertEqual(player.hands[player.hand_id].cards[0].rank, "K")
        self.assertEqual(player.hands[player.hand_id].cards[0].suit, "spades")

    def test_get_hand_value(self):
        player = Player("Adrian Nowak")
        card = Card("A", "Spades")
        player.add_card(card)
        player.add_card(card)

        self.assertEqual(player.get_hand_value(), 12)

        player.add_card(Card("10", "Diamonds"))
        self.assertEqual(player.get_hand_value(), 12)

        player.add_card(Card("10", "Clubs"))
        self.assertEqual(player.get_hand_value(), 22)

    def test_can_play(self):
        player = Player("Jakub Skoczek")
        player.money = 0

        self.assertFalse(player.can_play(20))

        player.money = 2137

        self.assertTrue(player.can_play(20))

    def test_reset_hand(self):
        player = Player("Barto Sitek")
        player.reset_hand(10)

        self.assertEqual(len(player.hands), 1)
        self.assertEqual(player.money, 990)
        self.assertEqual(player.hand_id, 0)
        self.assertEqual(player.insurance_bet, 0)
        self.assertFalse(player.is_insured)
        self.assertFalse(player.has_surrenderred)

    def test_can_stand(self):
        player = Player("Gukesh Domaraju")
        card = Card("A", "Spades")
        player.add_card(card)
        player.add_card(card)
        
        self.assertTrue(player.can_stand())

        player.add_card(Card("10", "Diamonds"))
        player.add_card(Card("10", "Clubs"))

        self.assertFalse(player.can_stand())

    def test_can_hit(self):
        player = Player("Jan Augustyn")
        card = Card("A", "Spades")
        player.add_card(card)
        player.add_card(card)

        self.assertTrue(player.can_hit())

        player.add_card(Card("10", "Diamonds"))
        player.add_card(Card("10", "Clubs"))

        self.assertFalse(player.can_hit())

    def test_hit(self):
        player = Player("Walter White")
        card = Card("8", "Hearts")
        player.add_card(card)
        player.add_card(card)

        result = player.hit(Card("2", "Clubs"))

        self.assertEqual(player.hands[player.hand_id].cards.__len__(), 3)
        self.assertTrue(result)

        result = player.hit(Card("10", "Diamonds"))

        self.assertEqual(player.hands[player.hand_id].cards.__len__(), 4)
        self.assertFalse(result)

    def test_can_double_down(self):
        player = Player("Saul Goodman")
        card = Card("8", "Hearts")
        player.add_card(card)
        player.add_card(card)

        self.assertTrue(player.can_double_down())

        player.add_card(card)

        self.assertFalse(player.can_double_down())

    def test_double_down(self):
        player = Player("Jesse Pinkman")
        player.reset_hand(10)
        card = Card("A", "Spades")
        player.add_card(card)
        player.add_card(card)

        result = player.double_down(Card("10", "Clubs"))

        self.assertEqual(player.hands[player.hand_id].cards.__len__(), 3)
        self.assertEqual(player.money, 980)
        self.assertFalse(result)

    def test_can_split(self):
        player = Player("Zupa")
        card1 = Card("A", "Spades")
        card2 = Card("A", "Hearts")
        player.add_card(card1)
        player.add_card(card2)

        self.assertTrue(player.can_split())

        player.add_card(Card("10", "Diamonds"))

        self.assertFalse(player.can_split())

    def test_split(self):
        player = Player("Gus Fring")
        player.reset_hand(10)
        card1 = Card("A", "Spades")
        card2 = Card("A", "Hearts")
        player.add_card(card1)
        player.add_card(card2)

        player.split(Card("10", "Clubs"), Card("10", "Diamonds"))

        self.assertEqual(len(player.hands), 2)
        self.assertEqual(player.hands[0].cards[0].rank, "A")
        self.assertEqual(player.hands[1].cards[0].rank, "A")
        self.assertEqual(player.hands[0].bet, 10)
        self.assertEqual(player.hands[1].bet, 10)
        self.assertEqual(player.hands[0].cards.__len__(), 2)
        self.assertEqual(player.hands[1].cards.__len__(), 2)
        self.assertEqual(player.money, 980)

    def test_split_not_possible(self):
        player = Player("Skam Wywial")
        player.reset_hand(10)
        card1 = Card("A", "Spades")
        card2 = Card("10", "Hearts")
        player.add_card(card1)
        player.add_card(card2)

        player.split(Card("10", "Clubs"), Card("10", "Diamonds"))

        self.assertEqual(len(player.hands), 1)
        self.assertEqual(player.hands[0].cards[0].rank, "A")
        self.assertEqual(player.hands[0].cards[1].rank, "10")
        self.assertEqual(player.hands[0].bet, 10)
        self.assertEqual(player.hands[0].cards.__len__(), 2)
        self.assertEqual(player.money, 990)

    def test_can_insurance(self):
        player = Player("Freddie Mercury")
        dealer = Dealer()
        dealer.add_card(Card("A", "Spades"))
        dealer.add_card(Card("Q", "eeen"))

        self.assertTrue(player.can_insurance(dealer.hand))

    def test_can_insurance_already_insured(self):
        player = Player("Brian May")
        dealer = Dealer()
        dealer.add_card(Card("A", "Spades"))
        dealer.add_card(Card("Q", "ueen"))
        player.is_insured = True

        self.assertFalse(player.can_insurance(dealer.hand))

    def test_insurance_not_possible(self):
        player = Player("Roger Taylor")
        dealer = Dealer()
        dealer.add_card(Card("Q", "ueen"))
        dealer.add_card(Card("Q", "ueen"))

        self.assertFalse(player.can_insurance(dealer.hand))

    def test_insurance(self):
        player = Player("John Deacon")
        dealer = Dealer()
        player.reset_hand(10)
        dealer.add_card(Card("A", "Spades"))
        dealer.add_card(Card("Q", "eeen"))

        player.insurance(dealer.hand)

        self.assertEqual(player.insurance_bet, 5)
        self.assertEqual(player.money, 985)
        self.assertTrue(player.is_insured)

    def test_can_surrender(self):
        player = Player("Lana Del Rey")
        card = Card("A", "Spades")
        player.add_card(card)
        player.add_card(card)

        self.assertTrue(player.can_surrender())

    def test_can_surrender_not_possible(self):
        player = Player("Post Malone")
        card = Card("A", "ustin")
        player.add_card(card)
        player.add_card(card)
        player.add_card(card)

        self.assertFalse(player.can_surrender())

    def test_surrender(self):
        player = Player("KrzakTV")
        player.reset_hand(10)
        card = Card("3", "spades")
        player.add_card(card)
        player.add_card(card)

        result = player.surrender()

        self.assertEqual(player.money, 995)
        self.assertTrue(player.has_surrenderred)
        self.assertFalse(result)

    def test_decide_action(self):
        player = Player("Fryderyk Chopin")
        deck = Deck()
        player.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer_hand = [deck.deal_card(), deck.deal_card()]

        action_suggestion = player.suggest_action(dealer_hand)
        action_suggestion2 = player.suggest_action(dealer_hand, True)

        self.assertIn(action_suggestion, ['HIT', 'DOUBLE DOWN', 'SPLIT', 'STAND'])
        self.assertIn(action_suggestion2, ['HIT', 'DOUBLE DOWN', 
                                           'SPLIT', 'STAND', 'HIT/DOUBLE DOWN', 'HIT/SPLIT', 
                                           'HIT/STAND', 'STAND/DOUBLE DOWN', 'STAND/SPLIT', 
                                           'DOUBLE DOWN/SPLIT', 'DOUBLE DOWN/STAND', 'SPLIT/STAND', 'UNKNOWN'])
