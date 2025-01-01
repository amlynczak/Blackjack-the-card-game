from .card import Card
from .hand import Hand
from card_counter.methods.canfield_master import CanfieldMasterCounter
from card_counter.methods.halves import HalvesCounter
from card_counter.methods.high_low import HighLowCounter
from card_counter.methods.high_optI import HighOptICounter
from card_counter.methods.omega import OmegaCounter
from card_counter.methods.revere_rapc import RevereRAPCCounter
from card_counter.methods.silver_fox import SilverFoxCounter
from card_counter.methods.zen_count import ZenCountCounter

import os
import json

class Player:
    def __init__(self, name, money = 1000):
        self.name = name
        self.hands = [Hand(name, bet = 0)]
        self.money = money
        self.hand_id = 0
        self.insurance_bet = 0
        self.is_insured = False
        self.has_surrenderred = False

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

        method = json.loads(open("assets/settings.json").read())["counting_method"]
        number_of_decks = json.loads(open("assets/settings.json").read())["number_of_decks"]
        self.counter = method_switch[method](number_of_decks)

    def add_card(self, card, hand_id = 0):
        self.hands[hand_id].add_card(card)

    def get_hand_value(self, hand_id = 0):
        return self.hands[hand_id].get_hand_value()
    
    def can_play(self, bet):
        return self.money >= bet

    def reset_hand(self, bet):
        self.hands.clear()
        self.hands = [Hand(self.name, bet)]
        self.money -= bet
        self.hand_id = 0
        self.insurance_bet = 0
        self.is_insured = False
        self.has_surrenderred = False

    def can_stand(self, hand_id = 0):
        return self.get_hand_value(hand_id) <= 21

    def can_hit(self, hand_id = 0):
        return self.get_hand_value(hand_id) < 21

    def hit(self, card, hand_id = 0):
        return self.hands[hand_id].hit(card)
    
    def can_double_down(self, hand_id = 0):
        return self.hands[self.hand_id].cards.__len__() == 2 and self.money >= self.hands[hand_id].bet
    
    def double_down(self, card, hand_id = 0):
        '''Player doubles down'''
        if self.can_double_down(hand_id):
            self.money -= self.hands[hand_id].bet
            return self.hands[hand_id].double_down(card)
    
    def can_split(self):
        return self.hands[self.hand_id].cards.__len__() == 2 and self.hands[self.hand_id].cards[0].rank == self.hands[self.hand_id].cards[1].rank and self.money >= self.hands[self.hand_id].bet
    
    def split(self, new_card1, new_card2):
        if self.can_split():
            original_hand = self.hands.pop(self.hand_id)
            self.money += original_hand.bet

            new_hand1 = Hand(original_hand.name + "-1", original_hand.bet)
            self.money -= original_hand.bet
            new_hand2 = Hand(original_hand.name + "-2", original_hand.bet)
            self.money -= original_hand.bet

            new_hand1.add_card(original_hand.cards[0])
            new_hand1.add_card(new_card1)
            new_hand2.add_card(original_hand.cards[1])
            new_hand2.add_card(new_card2)

            self.hands.append(new_hand1)
            self.hands.append(new_hand2)

    def can_insurance(self, dealer_hand):
        return dealer_hand[0].rank == 'A' and self.is_insured == False and self.money >= self.hands[self.hand_id].bet / 2

    def insurance(self, dealer_hand):
        if self.can_insurance(dealer_hand):
            self.insurance_bet = self.hands[self.hand_id].bet / 2
            self.money -= self.insurance_bet
            self.is_insured = True
    
    def can_surrender(self):
        return self.hands[self.hand_id].cards.__len__() == 2
    
    def surrender(self):
        if self.can_surrender():
            self.money += self.hands[self.hand_id].bet / 2
            self.has_surrenderred = True
        return False
    
    def decide_action(self, dealer_hand):
        hand_value = self.get_hand_value(self.hand_id)
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
                            break
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
                        if action == 'D' and not self.can_double_down():
                            action = 'H'
                        break

        return action

    def decide_action_based_on_count(self, dealers_hand):
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
                    return f'{action}/{self.more_aggressive(action)}'
            elif action_tmp[0] == '-':
                true_count_threshold = int(action_tmp[1:])
                if true_count <= ((-1) * true_count_threshold):
                    return f'{action}/{self.play_safe(action)}'

        return action

    def more_aggressive(self, action):
        if action == 'H':
            return 'D' if self.can_double_down() else 'H'
        elif action == 'S':
            return 'H'
        elif action == 'P':
            return 'P' if self.can_split() else 'S'
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

    def suggest_action(self, dealer_hand, counting=False):
        if counting:
            action = self.decide_action_based_on_count(dealer_hand)
        else:
            action = self.decide_action(dealer_hand)

        if action == 'H':
            return 'HIT'
        elif action == 'S':
            return 'STAND'
        elif action == 'D':
            return 'DOUBLE DOWN'
        elif action == 'P':
            return 'SPLIT'
        elif action == 'H/D':
            return 'HIT/DOUBLE DOWN'
        elif action == 'H/S':
            return 'HIT/STAND'
        elif action == 'H/P':
            return 'HIT/SPLIT'
        elif action == 'S/D':
            return 'STAND/DOUBLE DOWN'
        elif action == 'S/P':
            return 'STAND/SPLIT'
        elif action == 'S/H':
            return 'STAND/HIT'
        elif action == 'D/P':
            return 'DOUBLE DOWN/SPLIT'
        elif action == 'D/H':
            return 'DOUBLE DOWN/HIT'
        elif action == 'D/S':
            return 'DOUBLE DOWN/STAND'
        elif action == 'P/H':
            return 'SPLIT/HIT'
        elif action == 'P/D':
            return 'SPLIT/DOUBLE DOWN'
        elif action == 'P/S':
            return 'SPLIT/STAND'
        else:
            return 'UNKNOWN'
        

    def update_count(self, card):
        self.counter.update_count(card)

    def get_running_count(self):
        return self.counter.get_running_count()
    
    def get_true_count(self):
        return self.counter.get_count()

    def __str__(self):
        hand_str = ', '.join(str(card) for card in self.hands[self.hand_id].cards)
        return f"{self.name}: {hand_str} (Points: {self.get_hand_value()})"
