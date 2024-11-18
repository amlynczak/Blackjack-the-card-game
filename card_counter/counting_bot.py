from blackjack.player import Player
from card_counter.methods.high_low import HighLowCounter
import os

class CountingBot(Player):
    def __init__(self, method, name="Counting Bot", money = 1000):
        '''Initializes the bot with a name, hand, and money'''
        super().__init__(name, money)
        self.method = method
        self.count = 0

    def decide_action(self, dealers_hand):
        '''Decides whether to hit or stand based on the count'''
        count = self.method.get_count()
        if count >= 1:
            return "hit"
        else:
            return "stand"
        
    def update_count(self, card):
        '''Updates the count based on the card'''
        self.method.update_count(card)
