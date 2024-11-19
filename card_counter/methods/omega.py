from card_counter.counter import Counter

class OmegaCounter(Counter):
    def __init__(self):
        super().__init__()

    def card_value(self, card):
        if card.rank in ['2', '3', '7']:
            return 1
        elif card.rank in ['4', '5', '6']:
            return 2
        elif card.rank in ['8', 'A']:
            return 0
        elif card.rank in ['9']:
            return -1
        elif card.rank in ['10', 'J', 'Q', 'K']:
            return -2
        else:
            raise ValueError("Invalid card value")
        