from .card import Card
from .hand import Hand

class Player:
    def __init__(self, name):
        self.name = name
        self.hands = [Hand(name + "'s hand")]
        self.money = 1000
        self.bet = 0
        self.hand_id = 0

    def add_card(self, card, hand_id = 0):
        """Dodaje kartę do ręki gracza."""
        self.hands[hand_id].add_card(card)

    def get_hand_value(self, hand_id = 0):
        return self.hands[hand_id].get_hand_value()

    def reset_hand(self):
        """Czyści rękę gracza na potrzeby nowej rundy."""
        self.hands = [Hand(self.name + "'s hand")]

    def hit(self, card, hand_id = 0):
        return self.hands[hand_id].hit(card)
    
    def double_down(self, card):
        self.bet *= 2
        self.hit(card)
        return False
    
    def can_split(self):
        return len(self.hand) == 2 and self.hand[0].rank == self.hand[1].rank
    
    def split(self):
        if self.can_split():
            card = self.hand.pop()
            return Player(name=f"{self.name} (split)", hand=[card], money=self.money, bet=self.bet)
    
    def __str__(self):
        hand_str = ', '.join(str(card) for card in self.hands[0].cards)
        return f"{self.name}: {hand_str} (Punkty: {self.get_hand_value()})"
