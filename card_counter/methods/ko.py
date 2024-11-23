from card_counter.counter import Counter

class KOCounter(Counter):
    def __init__(self):
        super().__init__()

    def card_value(self, card):
        if card.rank in ['2', '3', '4', '5', '6', '7']:
            return 1
        elif card.rank in ['8', '9']:
            return 0
        elif card.rank in ['10', 'J', 'Q', 'K', 'A']:
            return -1
        else:
            raise ValueError("Invalid card value")
