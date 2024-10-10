from player import Player

class Dealer(Player):
    def __init__(self):
        super().__init__(name="Dealer")

    def should_hit(self):
        """Sprawdza, czy krupier powinien dobierać kartę (zgodnie z zasadami)."""
        return self.get_hand_value() < 17
