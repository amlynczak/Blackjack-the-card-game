from .card import Card
from .hand import Hand

class Player:
    def __init__(self, name):
        '''Initializes the player with a name, hand, and money'''
        self.name = name
        self.hands = [Hand(name + "'s hand")]
        self.money = 1000
        self.hand_id = 0
        self.standard_bet = 10

    def add_card(self, card, hand_id = 0):
        """Adds a card to the player's hand."""
        self.hands[hand_id].add_card(card)

    def get_hand_value(self, hand_id = 0):
        '''Calculates the value of the player's hand'''
        return self.hands[hand_id].get_hand_value()

    def reset_hand(self):
        """Clears the player's hand for a new round."""
        self.hands = [Hand(self.name + "'s hand")]
        self.money -= self.standard_bet
        self.hand_id = 0

    def hit(self, card, hand_id = 0):
        """Player takes a card from the deck."""
        return self.hands[hand_id].hit(card)
    
    def can_double_down(self, hand_id = 0):
        '''Checks if the player can double down'''
        return self.hands[self.hand_id].cards.__len__() == 2
    
    def double_down(self, card, hand_id = 0):
        '''Player doubles down'''
        if self.can_double_down(hand_id):
            self.money -= self.standard_bet
            return self.hands[hand_id].double_down(card)
    
    def can_split(self):
        '''Checks if the player can split'''
        return self.hands[self.hand_id].cards.__len__() == 2 and self.hands[self.hand_id].cards[0].rank == self.hands[self.hand_id].cards[1].rank
    
    def split(self, new_card1, new_card2):
        '''Player splits the hand'''
        if self.can_split():
            # Remove the hand to be split
            original_hand = self.hands.pop(self.hand_id)

            # Create two new hands
            new_hand1 = Hand(original_hand.name + " - 1")
            new_hand2 = Hand(original_hand.name + " - 2")

            # Add one card from the original hand to each new hand
            new_hand1.add_card(original_hand.cards[0])
            new_hand1.bet = self.standard_bet
            new_hand1.add_card(new_card1)
            new_hand2.add_card(original_hand.cards[1])
            new_hand2.bet = self.standard_bet
            new_hand2.add_card(new_card2)

            # Add the new hands to the player's hands
            self.hands.append(new_hand1)
            self.hands.append(new_hand2)

            for hand in self.hands:
                print(f"{hand.name}: {hand}")
    
    def __str__(self):
        '''Returns the player's name and hand'''
        hand_str = ', '.join(str(card) for card in self.hands[0].cards)
        return f"{self.name}: {hand_str} (Points: {self.get_hand_value()})"
