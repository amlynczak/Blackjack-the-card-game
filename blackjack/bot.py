from .player import Player
import random
import os

class Bot(Player):
    def __init__(self, name="Bot", money = 1000):
        super().__init__(name, money)
            
    def decide_final_action(self, dealer_hand):
        '''Decides the final action to take'''
        action  = self.decide_action(dealer_hand)
        r = random.uniform(0, 1)

        '''Bots are changing strategy 10% of the time'''
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
        '''Decides the bet amount (50% random, 50% standard)'''
        r = random.uniform(0, 1)
        if r <= 0.5:
            return standard_bet
        else:
            while True:
                bet_amounts = [10, 20, 50, 100, 200, 500]
                bet = random.choice(bet_amounts)
                if bet <= self.money:
                    return bet
