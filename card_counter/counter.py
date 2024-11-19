class Counter:
    def __init__(self):
        self.count = 0
        self.true_count = 0

    def reset(self):
        self.count = 0
        self.true_count = 0

    def update_count(self, card, num_decks):
        self.count += self.card_value(card)
        self.update_true_count(num_decks)

    def update_true_count(self, num_decks):
        self.true_count = self.count // (num_decks - 1)

    def get_count(self):
        return self.true_count