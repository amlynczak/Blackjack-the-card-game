from .card import Card
import random

class Deck:
    def __init__(self, number_of_decks=1):
        self.number_of_decks = number_of_decks
        self.cards = []
        self.build_deck()

    def build_deck(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for i in range(self.number_of_decks):
            for suit in suits:
                for rank in ranks:
                    self.cards.append(Card(rank, suit))
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) == 0:
            self.build_deck()
        return self.cards.pop()
    
    def remaining_cards(self):
        return len(self.cards)
    