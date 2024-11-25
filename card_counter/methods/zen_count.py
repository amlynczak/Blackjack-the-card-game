from card_counter.counter import Counter

class ZenCountCounter(Counter):
    def __init__(self, num_decks):
        super().__init__(num_decks)

    def card_value(self, card):
        if card.rank in ['2', '3', '7']:
            return 1
        elif card.rank in ['4', '5', '6']:
            return 2
        elif card.rank in ['8', '9']:
            return 0
        elif card.rank in ['10', 'J', 'Q', 'K']:
            return -2
        elif card.rank in ['A']:
            return -1
        else:
            raise ValueError("Invalid card value")