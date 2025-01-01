from .card import Card
import random

class Deck:
    def __init__(self, number_of_decks=1):
        self.number_of_decks = number_of_decks #number of decks vary from 1 to 8
        self.cards = []
        self.build_deck()

    def build_deck(self):
        suits = ["hearts", "diamonds", "clubs", "spades"]
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for i in range(self.number_of_decks):
            for suit in suits:
                for rank in ranks:
                    self.cards.append(Card(rank, suit))
        random.shuffle(self.cards) #shuffling the deck

    def deal_card(self):
        if len(self.cards) == 0: #if the deck is empty, build a new deck
            self.build_deck()
        return self.cards.pop()

    def deal_card_and_update_counts(self, players):
        '''used when card counting is enabled'''
        card = self.deal_card()
        for player in players:
            player.update_count(card)
        return card