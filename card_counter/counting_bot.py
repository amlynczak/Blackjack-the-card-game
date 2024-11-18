from blackjack.player import Player
import os

class CountingBot(Player):
    def __init__(self, method, name="Counting Bot", money = 1000):
        '''Initializes the bot with a name, hand, and money'''
        super().__init__(name, money)
        self.method = method

    def decide_action(self, dealers_hand):
        return "U"
