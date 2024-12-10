from .card import Card
from .hand import Hand
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
import json

class Player:
    def __init__(self, name, method, money = 1000):
        '''Initializes the player with a name, hand, and money'''
        self.name = name
        self.hands = [Hand(name, bet = 0)]
        self.money = money
        self.hand_id = 0
        self.insurance_bet = 0
        self.is_insured = False
        self.has_surrenderred = False

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

        method = json.loads(open("assets/settings.json").read())["counting_method"]
        number_of_decks = json.loads(open("assets/settings.json").read())["number_of_decks"]
        self.counter = method_switch[method](number_of_decks)

    def add_card(self, card, hand_id = 0):
        """Adds a card to the player's hand."""
        self.hands[hand_id].add_card(card)

    def get_hand_value(self, hand_id = 0):
        '''Calculates the value of the player's hand'''
        return self.hands[hand_id].get_hand_value()
    
    def can_play(self, bet):
        return self.money >= bet

    def reset_hand(self, bet):
        """Clears the player's hand for a new round."""
        self.hands.clear()
        self.hands = [Hand(self.name, bet)]
        self.money -= bet
        self.hand_id = 0
        self.insurance_bet = 0
        self.is_insured = False
        self.has_surrenderred = False

    def can_stand(self):
        return self.get_hand_value() <= 21

    def can_hit(self, hand_id = 0):
        return self.get_hand_value(hand_id) < 21

    def hit(self, card, hand_id = 0):
        """Player takes a card from the deck."""
        return self.hands[hand_id].hit(card)
    
    def can_double_down(self, hand_id = 0):
        '''Checks if the player can double down'''
        return self.hands[self.hand_id].cards.__len__() == 2 and self.money >= self.hands[hand_id].bet
    
    def double_down(self, card, hand_id = 0):
        '''Player doubles down'''
        if self.can_double_down(hand_id):
            self.money -= self.hands[hand_id].bet
            return self.hands[hand_id].double_down(card)
    
    def can_split(self):
        '''Checks if the player can split'''
        return self.hands[self.hand_id].cards.__len__() == 2 and self.hands[self.hand_id].cards[0].rank == self.hands[self.hand_id].cards[1].rank and self.money >= self.hands[self.hand_id].bet
    
    def split(self, new_card1, new_card2):
        '''Player splits the hand'''
        if self.can_split():
            # Remove the hand to be split
            original_hand = self.hands.pop(self.hand_id)
            self.money += original_hand.bet

            # Create two new hands
            new_hand1 = Hand(original_hand.name + "-1", original_hand.bet)
            self.money -= original_hand.bet
            new_hand2 = Hand(original_hand.name + "-2", original_hand.bet)
            self.money -= original_hand.bet

            # Add one card from the original hand to each new hand
            new_hand1.add_card(original_hand.cards[0])
            new_hand1.add_card(new_card1)
            new_hand2.add_card(original_hand.cards[1])
            new_hand2.add_card(new_card2)

            # Add the new hands to the player's hands
            self.hands.append(new_hand1)
            self.hands.append(new_hand2)

            for hand in self.hands:
                print(f"{hand.name}: {hand}")

    def can_insurance(self, dealer_hand):
        '''Checks if the player can take insurance'''
        return dealer_hand[0].rank == 'A' and self.is_insured == False and self.money >= self.hands[self.hand_id].bet / 2

    def insurance(self, dealer_hand):
        '''Player takes insurance'''
        if self.can_insurance(dealer_hand):
            self.insurance_bet = self.hands[self.hand_id].bet / 2
            self.money -= self.insurance_bet
            self.is_insured = True
    
    def can_surrender(self):
        '''Checks if the player can surrender'''
        return self.hands[self.hand_id].cards.__len__() == 2
    
    def surrender(self):
        '''Player surrenders'''
        if self.can_surrender():
            self.money += self.hands[self.hand_id].bet / 2
            self.has_surrenderred = True
        return False
    
    def suggest_action(self, dealers_card):
        hand_value = self.get_hand_value()
        rank_to_num = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
        dealer_card_rank = dealers_card.rank
        dealers_card_num = rank_to_num[dealer_card_rank]
        suggested_action = 'U'

        if self.hands[self.hand_id].cards[0].rank == self.hands[self.hand_id].cards[1].rank and len(self.hands[self.hand_id].cards) == 2:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/basic_strategy/pairs")
        elif 'A' in [card.rank for card in self.hands[self.hand_id].cards] and len(self.hands[self.hand_id].cards) == 2:
            non_ace_card = [card for card in self.hands[self.hand_id].cards if card.rank != 'A'][0]
            file_path = os.path.join(os.path.dirname(__file__), "../assets/basic_strategy/pairs_with_aces")
        else:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/basic_strategy/points")

        with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(self.hands[self.hand_id].cards[0].rank):
                        suggested_action = line.split()[dealers_card_num]
                        break
        
        if suggested_action == 'H':
            suggested_action = 'hit'
        elif suggested_action == 'S':
            suggested_action = 'stand'
        elif suggested_action == 'P':
            suggested_action = 'split'
        elif suggested_action == 'D':
            suggested_action = 'double down'

        return suggested_action

    def __str__(self):
        '''Returns the player's name and hand'''
        hand_str = ', '.join(str(card) for card in self.hands[self.hand_id].cards)
        return f"{self.name}: {hand_str} (Points: {self.get_hand_value()})"
