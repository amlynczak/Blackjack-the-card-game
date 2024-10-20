class Hand:
    def __init__(self, hand_name):
        self.cards = []
        self.name = hand_name

    def add_card(self, card):
        """Dodaje kartę do ręki."""
        self.cards.append(card)

    def get_hand_value(self):
        """Oblicza wartość punktową ręki, traktując Asa jako 1 lub 11."""
        value = 0
        num_aces = 0
        for card in self.cards:
            value += card.value()
            if card.rank == 'A':
                num_aces += 1

        # Jeśli mamy Asy i suma przekracza 21, traktujemy niektóre Asy jako 1
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value
    
    def hit(self, card):
        self.add_card(card)
        print(f"{card} for {self.name}")
        print(f"{self.name}: {self}")

        if self.get_hand_value() > 21:
            print(f"{self.name} przekroczył 21! Przegrywasz.")
            return False
        return True
    
    def __str__(self):
        hand_str = ', '.join(str(card) for card in self.cards)
        return f"{hand_str} (Punkty: {self.get_hand_value()})"