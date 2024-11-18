class HighLowCounter:
    def __init__(self):
        self.count = 0
        self.true_count = 0

    def reset(self):
        self.count = 0
        self.true_count = 0

    def card_value(self, card):
        if card in ['2', '3', '4', '5', '6']:
            return 1
        elif card in ['7', '8', '9']:
            return 0
        elif card in ['10', 'J', 'Q', 'K', 'A']:
            return -1
        else:
            raise ValueError("Invalid card value")

    def update_count(self, card, num_decks):
        self.count += self.card_value(card)
        self.update_true_count(num_decks)

    def update_true_count(self, num_decks):
        self.true_count = self.count // (num_decks - 1)

    def get_count(self):
        return self.true_count