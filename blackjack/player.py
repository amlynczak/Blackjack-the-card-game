from .card import Card

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.money = 1000
        self.bet = 0

    def add_card(self, card):
        """Dodaje kartę do ręki gracza."""
        self.hand.append(card)

    def get_hand_value(self):
        """Oblicza wartość punktową ręki gracza, traktując Asa jako 1 lub 11."""
        value = 0
        num_aces = 0
        for card in self.hand:
            value += card.value()
            if card.rank == 'A':
                num_aces += 1

        # Jeśli mamy Asy i suma przekracza 21, traktujemy niektóre Asy jako 1
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value

    def reset_hand(self):
        """Czyści rękę gracza na potrzeby nowej rundy."""
        self.hand = []

    def hit(self, card):
        self.add_card(card)
        print(f"{card} for {self.name}")
        print(f"{self.name}: {self}")

        if self.get_hand_value() > 21:
            print(f"{self.name} przekroczył 21! Przegrywasz.")
            return False
        return True
    
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
        hand_str = ', '.join(str(card) for card in self.hand)
        return f"{self.name}: {hand_str} (Punkty: {self.get_hand_value()})"
