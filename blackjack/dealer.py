from .player import Player

class Dealer():
    def __init__(self):
        self.name = "Dealer"
        self.hand = []

    def add_card(self, card):
        """Dodaje kartę do ręki krupiera."""
        self.hand.append(card)

    def get_hand_value(self):
        """Oblicza wartość punktową ręki krupiera, traktując Asa jako 1 lub 11."""
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
    
    def dealers_turn(self, deck):
        """Tura krupiera - krupier dobiera karty zgodnie z zasadami."""
        print(f"Karty Dealera: {self}")
        while self.should_hit():
            card = deck.deal_card()
            self.add_card(card)
            print(f"Dealer dobrał kartę: {card}")
        print(f"Ręka Dealera: {self}")
    
    def reset_hand(self):
        """Czyści rękę krupiera na potrzeby nowej rundy."""
        self.hand = []

    def should_hit(self):
        """Sprawdza, czy krupier powinien dobierać kartę (zgodnie z zasadami)."""
        return self.get_hand_value() < 17
    
    def __str__(self):
        hand_str = ', '.join(str(card) for card in self.hand)
        return f"{self.name}: {hand_str} (Punkty: {self.get_hand_value()})"
