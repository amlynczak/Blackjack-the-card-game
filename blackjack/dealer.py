import time

from .player import Player

from ui.utils import display_game_state

class Dealer():
    def __init__(self):
        '''Initializes the dealer with a name and an empty hand'''
        self.name = "Dealer"
        self.hand = []

    def add_card(self, card):
        """Adds a card to the dealer's hand."""
        self.hand.append(card)

    def get_hand_value(self):
        """Calculates the value of the dealer's hand with aces handled."""
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
    
    def dealers_turn(self, deck, screen, main_player, bot_players):
        """Starts the dealer's turn, dealing cards until the value is at"""
        print(f"Dealer's cards: {self}")
        while self.should_hit():
            card = deck.deal_card()
            self.add_card(card)
            print(f"Dealer hits: {card}")
            time.sleep(3)
            display_game_state(screen, main_player, self, bot_players, True)
        print(f"Dealer's hand: {self}")
    
    def reset_hand(self):
        """Clears the dealer's hand for a new round."""
        self.hand = []

    def should_hit(self):
        """Returns True if the dealer should hit, False otherwise."""
        return self.get_hand_value() < 17
    
    def __str__(self):
        '''Returns a string representation of the dealer's hand'''
        hand_str = ', '.join(str(card) for card in self.hand)
        return f"{self.name}: {hand_str} (Points: {self.get_hand_value()})"
