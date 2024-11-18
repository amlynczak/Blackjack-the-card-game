class KnockOutCounter:
    def __init__(self):
        self.reset()

    def reset(self):
        self.count = 0

    def card_value(self, card):
        if card in ['2', '3', '4', '5', '6', '7']:
            return 1
        elif card in ['8', '9']:
            return 0
        elif card in ['10', 'J', 'Q', 'K', 'A']:
            return -1
        else:
            raise ValueError("Invalid card value")

    def update_count(self, card):
        self.count += self.card_value(card)

    def get_count(self):
        return self.count
