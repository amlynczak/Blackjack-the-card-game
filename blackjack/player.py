from .card import Card
from .hand import Hand

class Player:
    def __init__(self, name, money = 1000):
        '''Initializes the player with a name, hand, and money'''
        self.name = name
        self.hands = [Hand(name + "'s hand", bet = 0)]
        self.money = money
        self.hand_id = 0
        self.insurance_bet = 0
        self.isInsured = False
        self.has_surrenderred = False

    def add_card(self, card, hand_id = 0):
        """Adds a card to the player's hand."""
        self.hands[hand_id].add_card(card)

    def get_hand_value(self, hand_id = 0):
        '''Calculates the value of the player's hand'''
        return self.hands[hand_id].get_hand_value()

    def reset_hand(self, standard_bet):
        """Clears the player's hand for a new round."""
        self.hands = [Hand(self.name + "'s hand", standard_bet)]
        self.money -= standard_bet
        self.hand_id = 0
        self.insurance_bet = 0
        self.isInsured = False
        self.has_surrenderred = False

    def hit(self, card, hand_id = 0):
        """Player takes a card from the deck."""
        return self.hands[hand_id].hit(card)
    
    def can_double_down(self, hand_id = 0):
        '''Checks if the player can double down'''
        return self.hands[self.hand_id].cards.__len__() == 2
    
    def double_down(self, card, hand_id = 0):
        '''Player doubles down'''
        if self.can_double_down(hand_id):
            self.money -= self.hands[hand_id].bet
            return self.hands[hand_id].double_down(card)
    
    def can_split(self):
        '''Checks if the player can split'''
        return self.hands[self.hand_id].cards.__len__() == 2 and self.hands[self.hand_id].cards[0].rank == self.hands[self.hand_id].cards[1].rank
    
    def split(self, new_card1, new_card2):
        '''Player splits the hand'''
        if self.can_split():
            # Remove the hand to be split
            original_hand = self.hands.pop(self.hand_id)
            self.money += original_hand.bet

            # Create two new hands
            new_hand1 = Hand(original_hand.name + " - 1", original_hand.bet)
            self.money -= original_hand.bet
            new_hand2 = Hand(original_hand.name + " - 2", original_hand.bet)
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
        return dealer_hand[0].rank == 'A' and self.isInsured == False

    def insurance(self, dealer_hand):
        '''Player takes insurance'''
        if self.can_insurance(dealer_hand):
            self.insurance_bet = self.hands[self.hand_id].bet / 2
            self.money -= self.insurance_bet
            self.isInsured = True
    
    def can_surrender(self):
        '''Checks if the player can surrender'''
        return self.hands[self.hand_id].cards.__len__() == 2
    
    def surrender(self):
        '''Player surrenders'''
        if self.can_surrender():
            self.money += self.hands[self.hand_id].bet / 2
            self.has_surrenderred = True
        return False

    def __str__(self):
        '''Returns the player's name and hand'''
        hand_str = ', '.join(str(card) for card in self.hands[0].cards)
        return f"{self.name}: {hand_str} (Points: {self.get_hand_value()})"
