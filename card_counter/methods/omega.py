class OmegaCounter:
    def __init__(self):
        self.reset()

    def reset(self):
        self.count = 0

    def card_value(self, card):
        if card in ['2', '3']:
            return 1
        elif card in ['4', '5', '6']:
            return 2
        elif card in ['7']:
            return 1
        elif card in ['8']:
            return 0
        elif card in ['9']:
            return -1
        elif card in ['10', 'J', 'Q', 'K']:
            return -2
        elif card in ['A']:
            return 0
        else:
            raise ValueError("Invalid card value")
        
    def update_count(self, card):
        self.count += self.card_value(card)

    def get_count(self):
        return self.count