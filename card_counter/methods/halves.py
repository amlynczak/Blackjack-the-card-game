from card_counter.counter import Counter

class HalvesCounter(Counter):
    def __init__(self):
        super().__init__()

    def card_value(self, card):
        if card.rank in ['2', '7']:
            return 0.5
        elif card.rank in ['3', '4', '6']:
            return 1
        elif card.rank in ['5']:
            return 1.5
        elif card.rank in ['8']:
            return 0
        elif card.rank in ['9']:
            return -0.5
        elif card.rank in ['10', 'J', 'Q', 'K', 'A']:
            return -1
        else:
            raise ValueError("Invalid card value")