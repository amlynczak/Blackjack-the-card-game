from .player import Player
import random
import os

class Bot(Player):
    def __init__(self, name="Bot", money = 1000):
        '''Initializes the bot with a name, hand, and money'''
        super().__init__(name, money)
            
    def decide_final_action(self, dealer_hand):
        action  = self.decide_action(dealer_hand)
        print("action in bot: ", action)
        r = random.uniform(0, 1)

        if action == 'H' and r <= 0.9:
            return 'hit'
        elif action == 'D' and r <= 0.9:
            return 'double'
        elif action == 'P' and r <= 0.9:
            return 'split'
        elif action == 'S' and r <= 0.9:
            return 'stand'
        else:
            if self.get_hand_value() < 17:
                return 'hit'
            else:
                return 'stand'
            
    def decide_bet(self, standard_bet):
        '''Decides the bet to place based on the standard bet'''
        r = random.uniform(0, 1)
        if r <= 0.9:
            return standard_bet
        else:
            return standard_bet * random.randint(1, 5)
