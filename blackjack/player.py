from .card import Card

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

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
    
    def __str__(self):
        hand_str = ', '.join(str(card) for card in self.hand)
        return f"{self.name}: {hand_str} (Punkty: {self.get_hand_value()})"
