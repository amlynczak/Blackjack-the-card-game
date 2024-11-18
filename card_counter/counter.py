class CardCounter:
    def __init__(self):
        self.count = 0
        self.card_values = {
            '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
            '7': 0, '8': 0, '9': 0,
            '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
        }

    def update_count(self, card):
        if card in self.card_values:
            self.count += self.card_values[card]
        else:
            raise ValueError(f"Unknown card: {card}")

    def get_count(self):
        return self.count

    def reset_count(self):
        self.count = 0

# Example usage:
if __name__ == "__main__":
    counter = CardCounter()
    cards = ['10', 'J', 'A', '3', '5', '7']
    for card in cards:
        counter.update_count(card)
        print(f"Card: {card}, Current Count: {counter.get_count()}")