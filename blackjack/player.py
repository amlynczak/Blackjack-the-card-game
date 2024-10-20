from .card import Card
from .hand import Hand

class Player:
    def __init__(self, name):
        self.name = name
        self.hands = [Hand(name + "'s hand")]
        self.money = 1000
        self.hand_id = 0
        self.standard_bet = 10

    def add_card(self, card, hand_id = 0):
        """Dodaje kartę do ręki gracza."""
        self.hands[hand_id].add_card(card)

    def get_hand_value(self, hand_id = 0):
        return self.hands[hand_id].get_hand_value()

    def reset_hand(self):
        """Czyści rękę gracza na potrzeby nowej rundy."""
        self.hands = [Hand(self.name + "'s hand")]
        self.money -= self.standard_bet
        self.hand_id = 0

    def hit(self, card, hand_id = 0):
        return self.hands[hand_id].hit(card)
    
    def can_double_down(self, hand_id = 0):
        return self.hands[self.hand_id].cards.__len__() == 2
    
    def double_down(self, card, hand_id = 0):
        if self.can_double_down(hand_id):
            self.money -= self.standard_bet
            return self.hands[hand_id].double_down(card)
    
    def can_split(self):
        return self.hands[self.hand_id].cards.__len__() == 2 and self.hands[self.hand_id].cards[0].rank == self.hands[self.hand_id].cards[1].rank
    
    def split(self, new_card1, new_card2):
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
        hand_str = ', '.join(str(card) for card in self.hands[0].cards)
        return f"{self.name}: {hand_str} (Punkty: {self.get_hand_value()})"
