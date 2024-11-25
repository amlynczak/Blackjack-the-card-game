from card_counter.counter import Counter

class HighOptICounter(Counter):
    def __init__(self, num_decks):
        super().__init__(num_decks)

    def card_value(self, card):
        if card.rank in ['2', '7', '8', '9', 'A']:
            return 0
        elif card.rank in ['3', '4', '6']:
            return 1
        elif card.rank in ['10', 'J', 'Q', 'K']:
            return -1
        else:
            raise ValueError("Invalid card value")