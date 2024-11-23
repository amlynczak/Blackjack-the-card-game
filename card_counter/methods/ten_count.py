from card_counter.counter import Counter

class TenCountCounter(Counter):
    def __init__(self):
        super().__init__()

    def card_value(self, card):
        if card.rank in ['2', '3', '4', '5', '6', '7', '8', '9', 'A']:
            return 1
        elif card.rank in ['10', 'J', 'Q', 'K']:
            return -2
        else:
            raise ValueError("Invalid card value")
