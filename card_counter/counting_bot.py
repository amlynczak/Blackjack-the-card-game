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

class CountingBot(Bot):
    def __init__(self, name="Counting Bot", money = 1000, method = 'high_low', number_of_decks = 1):
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

        self.counter = method_switch[method](number_of_decks)

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
        elif 'A' in [card.rank for card in self.hands[self.hand_id].cards] and len(self.hands[self.hand_id].cards) == 2:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/counting_cards/pairs_with_aces")
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(self.hands[self.hand_id].cards[0].rank):
                        action_tmp = line.split()[dealer_card_num]
        else:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/counting_cards/points")
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(str(hand_value)):
                        action_tmp = line.split()[dealer_card_num]
        
        true_count = self.counter.get_count()
        print(true_count)

        if action != action_tmp:
            if action_tmp[0] == '+':
                true_count_threshold = int(action_tmp[1:])
                if true_count >= true_count_threshold:
                    action = self.convert_action(action, True)
            elif action_tmp[0] == '-':
                true_count_threshold = int(action_tmp[1:])
                if true_count <= ((-1) * true_count_threshold):
                    action = self.convert_action(action, False)

        if action == 'H':
            return 'hit'
        elif action == 'S':
            return 'stand'
        elif action == 'D':
            return 'double'
        elif action == 'P':
            return 'split'
        elif action == 'I':
            return 'insurance'
        elif action == 'R':
            return 'surrender'

    def convert_action(self, action, up = True):
        if action == 'H' and up:
            return 'D'
        elif action == 'H' and not up:
            return 'S'
        elif action == 'S' and up:
            return 'H'
        elif action == 'D' and not up:
            return 'H'
        elif action == 'P' and not up:
            return 'H'
        
        return action #TODO do proper conversion

        
    def update_count(self, card):
        '''Updates the count based on the card'''
        self.counter.update_count(card)
