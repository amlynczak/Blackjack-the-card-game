from blackjack.bot import Bot
from card_counter.methods import TenCountCounter, HalvesCounter, HighLowCounter, HighOptICounter, HighOptIICounter
from card_counter.methods import KOCounter, OmegaIICounter, Red7Counter, ZenCountCounter
import os

class CountingBot(Bot):
    def __init__(self, name="Counting Bot", money = 1000, counter = TenCountCounter()):
        '''Initializes the bot with a name, hand, and money'''
        super().__init__(name, money)
        self.counter = counter

    def decide_final_action(self, dealers_hand):
        '''Decides whether to hit or stand based on the count'''
        action = self.decide_action(dealers_hand)

        hand_value = self.get_hand_value(self.hand_id)
        rank_to_num = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
        
        dealer_card_rank = dealers_hand[0].rank
        dealer_card_num = rank_to_num[dealer_card_rank]

        if self.hands[self.hand_id].cards[0].rank == self.hands[self.hand_id].cards[1].rank and len(self.hands[self.hand_id].cards) == 2:
            file_path = os.path.join(os.path.dirname(__file__), "../assets/counting_cards/pairs")
            with open(file_path, 'r') as file:
                for line in file:
                    if line.startswith(self.hands[self.hand_id].cards[0].rank):
                        action_tmp = line.split()[dealer_card_num]
                        if action == action_tmp:
                            break
                        else:
                            break

        #TODO: Implement the rest of the cases


        
    def update_count(self, card):
        '''Updates the count based on the card'''
        self.counter.update_count(card)
