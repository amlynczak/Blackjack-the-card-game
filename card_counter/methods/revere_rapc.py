from card_counter.counter import Counter

class RevereRAPCCounter(Counter):
    def __init__(self, num_decks):
        super().__init__(num_decks)

    def card_value(self, card):
        if card.rank in ['2', '7']:
            return 2
        elif card.rank in ['3', '4', '6']:
            return 3
        elif card.rank in ['5']:
            return 4
        elif card.rank in ['8']:
            return 0
        elif card.rank in ['9']:
            return -1
        elif card.rank in ['10', 'J', 'Q', 'K']:
            return -3
        elif card.rank in ['A']:
            return -4
        else:
            raise ValueError("Invalid card value")