from .player import Player
import random
import os

class Bot(Player):
    def __init__(self, name="Bot", money = 1000):
        '''Initializes the bot with a name, hand, and money'''
        super().__init__(name, money)

    def decide_action(self, dealer_hand):
        '''Decides the action to take based on the dealer's hand'''
        hand_value = self.get_hand_value()
        rank_to_num = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
        
        dealer_card_rank = dealer_hand[0].rank
        dealer_card_num = rank_to_num[dealer_card_rank]
        action = 'U' #unknown

        if self.hands[self.hand_id].cards[0].rank ==  self.hands[self.hand_id].cards[1].rank and len(self.hands[self.hand_id].cards) == 2:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/basic_strategy/pairs")
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(self.hands[self.hand_id].cards[0].rank):
                        action = line.split()[dealer_card_num]
                        if self.can_split() and action == 'P':
                            break
                        else:
                            action = 'U'
        elif 'A' in [card.rank for card in self.hands[self.hand_id].cards] and len(self.hands[self.hand_id].cards) == 2:
            non_ace_card = [card for card in self.hands[self.hand_id].cards if card.rank != 'A'][0]
            file_path = os.path.join(os.path.dirname(__file__), "../assets/basic_strategy/pairs_with_aces")
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(non_ace_card.rank):
                        action = line.split()[dealer_card_num]
                        break
        else:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/basic_strategy/points")
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(str(hand_value)):
                        action = line.split()[dealer_card_num]
                        break

        if action == 'H':
            return 'hit'
        elif action == 'D':
            return 'double'
        elif action == 'P':
            return 'split'
        elif action == 'S':
            return 'stand'
        else:
            if hand_value < 17:
                return 'hit'
            else:
                return 'stand'