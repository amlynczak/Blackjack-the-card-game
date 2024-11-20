from blackjack.player import Player
from card_counter.methods import TenCountCounter, HalvesCounter, HighLowCounter, HighOptICounter, HighOptIICounter
from card_counter.methods import KOCounter, OmegaIICounter, Red7Counter, ZenCountCounter
import os

class CountingBot(Player):
    def __init__(self, name="Counting Bot", money = 1000, counter = TenCountCounter()):
        '''Initializes the bot with a name, hand, and money'''
        super().__init__(name, money)
        self.counter = counter

    def decide_action(self, dealers_hand):
        '''Decides whether to hit or stand based on the count'''
        count = self.method.get_count()
        if count >= 1:
            return "hit"
        else:
            return "stand"
        
    def update_count(self, card):
        '''Updates the count based on the card'''
        self.counter.update_count(card)
