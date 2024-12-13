from blackjack.bot import Bot
from card_counter.methods.halves import HalvesCounter
from card_counter.methods.high_low import HighLowCounter
from card_counter.methods.high_optI import HighOptICounter
from card_counter.methods.high_optII import HighOptIICounter
from card_counter.methods.ko import KOCounter
from card_counter.methods.omega import OmegaCounter
from card_counter.methods.red_seven import Red7Counter
from card_counter.methods.ten_count import TenCountCounter
from card_counter.methods.zen_count import ZenCountCounter


import os
import random

class CountingBot(Bot):
    def __init__(self, name="Counting Bot", money = 1000, number_of_decks = 1):
        '''Initializes the bot with a name, hand, and money'''
        super().__init__(name, money)
        method_switch = {
            'halves': HalvesCounter,
            'high_low': HighLowCounter,
            'high_optI': HighOptICounter,
            'high_optII': HighOptIICounter,
            'ko': KOCounter,
            'omega': OmegaCounter,
            'red_seven': Red7Counter,
            'ten_count': TenCountCounter,
            'zen_count': ZenCountCounter
        }

        self.counter = method_switch[random.choice(list(method_switch.keys()))](number_of_decks)

    def decide_final_action(self, dealers_hand):
        '''Decides whether to hit or stand based on the count'''
        action = self.decide_action(dealers_hand)

        hand_value = self.get_hand_value(self.hand_id)
        rank_to_num = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
        
        dealer_card_rank = dealers_hand[0].rank
        dealer_card_num = rank_to_num[dealer_card_rank]

        action_tmp = 'U' #unknown

        if self.hands[self.hand_id].cards[0].rank == self.hands[self.hand_id].cards[1].rank and len(self.hands[self.hand_id].cards) == 2:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/counting_cards/pairs")
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(self.hands[self.hand_id].cards[0].rank):
                        action_tmp = line.split()[dealer_card_num]
                        print("split deciding")
                        break
        elif 'A' in [card.rank for card in self.hands[self.hand_id].cards] and len(self.hands[self.hand_id].cards) == 2:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/counting_cards/pairs_with_aces")
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(self.hands[self.hand_id].cards[0].rank):
                        action_tmp = line.split()[dealer_card_num]
                        print("ace deciding")
                        break
        else:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/counting_cards/points")
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(str(hand_value)):
                        action_tmp = line.split()[dealer_card_num]
                        print("point deciding")
                        break

        print(action)
        print(action_tmp)
        
        true_count = self.counter.get_count()
        print(true_count)

        if action != action_tmp:
            if action_tmp[0] == '+':
                true_count_threshold = int(action_tmp[1:])
                if true_count >= true_count_threshold:
                    print("more aggressive")
                    action = self.more_aggressive(action)
            elif action_tmp[0] == '-':
                true_count_threshold = int(action_tmp[1:])
                if true_count <= ((-1) * true_count_threshold):
                    print("play safe")
                    action = self.play_safe(action)

        if action == 'H':
            return 'hit'
        elif action == 'S':
            return 'stand'
        elif action == 'D':
            return 'double'
        elif action == 'P':
            return 'split'

    def more_aggressive(self, action):
        if action == 'H':
            return 'D' if self.can_double_down() else 'H'
        elif action == 'S':
            return 'H'
        elif action == 'P':
            return 'P'
        elif action == 'D':
            return 'D'
        
    def play_safe(self, action):
        if action == 'H':
            return 'S'
        elif action == 'S':
            return 'S'
        elif action == 'D':
            return 'H'
        elif action == 'P':
            return 'H'

    def decide_bet(self, standard_bet):
        true_count = self.counter.get_count()
        file_path = os.path.join(os.path.dirname(__file__), "../assets/counting_cards/casino_adv")
        bet = standard_bet
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith(str(int(true_count))):
                    bet = round(float(line.split()[1]) * self.money * (-1) / 5) * 5
                    break
        if bet > self.money or bet < standard_bet:
            return standard_bet
        else:
            return bet

    def update_count(self, card):
        '''Updates the count based on the card'''
        self.counter.update_count(card)
