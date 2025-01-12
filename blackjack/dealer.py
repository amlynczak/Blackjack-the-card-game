import time

from ui.utils import display_game_state

'''
Class representing the dealer in the game.
'''
class Dealer():
    def __init__(self):
        self.name = "Dealer"
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def get_hand_value(self):
        """Returns the value of the dealer's hand, converting aces to 1 if the value is over 21."""
        value = 0
        num_aces = 0
        for card in self.hand:
            value += card.value()
            if card.rank == 'A':
                num_aces += 1

        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value
    
    def dealers_turn(self, deck, screen, main_player, bot_players, counting_prohibited=True):
        while self.should_hit():
            if counting_prohibited: #based on this parameter, the counts will be updated or not
                card = deck.deal_card()
            else:
                card = deck.deal_card_and_update_counts(bot_players+[main_player])
            self.add_card(card)
            time.sleep(2) #delay for better user experience
            display_game_state(screen, main_player, self, bot_players, counting_prohibited, True, False)
    
    def reset_hand(self):
        self.hand = []

    def should_hit(self):
        '''Dealer stands on soft 17'''
        return self.get_hand_value() < 17
    
    def __str__(self):
        hand_str = ', '.join(str(card) for card in self.hand)
        return f"{self.name}: {hand_str} (Points: {self.get_hand_value()})"
