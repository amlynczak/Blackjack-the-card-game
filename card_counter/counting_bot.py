from blackjack.bot import Bot
from card_counter.methods.canfield_master import CanfieldMasterCounter
from card_counter.methods.halves import HalvesCounter
from card_counter.methods.high_low import HighLowCounter
from card_counter.methods.high_optI import HighOptICounter
from card_counter.methods.omega import OmegaCounter
from card_counter.methods.revere_rapc import RevereRAPCCounter
from card_counter.methods.silver_fox import SilverFoxCounter
from card_counter.methods.zen_count import ZenCountCounter

import os
import random

class CountingBot(Bot):
    def __init__(self, name="Counting Bot", money = 1000, number_of_decks = 1):
        super().__init__(name, money)
        method_switch = {
            'Canfield Master': CanfieldMasterCounter,
            'Halves': HalvesCounter,
            'High - Low': HighLowCounter,
            'High - Opt I': HighOptICounter,
            'Omega II': OmegaCounter,
            'Revere RAPC': RevereRAPCCounter,
            'Silver Fox': SilverFoxCounter,
            'Zen Count': ZenCountCounter
        }

        self.counter = method_switch[random.choice(list(method_switch.keys()))](number_of_decks)

    def decide_final_action(self, dealers_hand):
        if self.can_insurance and self.is_insured == False and self.counter.get_count() >= 3:
            return 'insurance'

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
                        break
        elif 'A' in [card.rank for card in self.hands[self.hand_id].cards] and len(self.hands[self.hand_id].cards) == 2:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/counting_cards/pairs_with_aces")
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(self.hands[self.hand_id].cards[0].rank):
                        action_tmp = line.split()[dealer_card_num]
                        break
        else:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/counting_cards/points")
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(str(hand_value)):
                        action_tmp = line.split()[dealer_card_num]
                        break
        
        true_count = self.counter.get_count()

        if action != action_tmp:
            if action_tmp[0] == '+':
                true_count_threshold = int(action_tmp[1:])
                if true_count >= true_count_threshold:
                    action = self.more_aggressive(action)
            elif action_tmp[0] == '-':
                true_count_threshold = int(action_tmp[1:])
                if true_count <= ((-1) * true_count_threshold):
                    action = self.play_safe(action)

        if action == 'H':
            return 'hit'
        elif action == 'S':
            return 'stand'
        elif action == 'D':
            return 'double'
        elif action == 'P':
            return 'split'
        else:
            if self.get_hand_value(self.hand_id) < 17:
                return 'hit'
            else:
                return 'stand'

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
                    bet = round(float(line.split()[1]) * self.money * (-1))
                    break
        if random.uniform(0, 1) <= 0.8:   
            if bet < 15:
                return 10
            elif bet >= 15 and bet < 35:
                return 20
            elif bet >= 35 and bet < 75:
                return 50
            elif bet >= 75 and bet < 150:
                return 100
            elif bet >= 150 and bet < 350:
                return 200
            elif bet >= 350:
                return 500
        else:
            while True:
                bet_amounts = [10, 20, 50, 100, 200, 500]
                bet = random.choice(bet_amounts)
                if bet <= self.money:
                    return bet

    def update_count(self, card):
        self.counter.update_count(card)
