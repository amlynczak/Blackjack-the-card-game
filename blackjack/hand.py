class Hand:
    def __init__(self, hand_name, bet):
        self.cards = []
        self.name = hand_name
        self.bet = bet
        self.isBlackjack = False
        self.has_doubled_down = False

    def add_card(self, card):
        self.cards.append(card)

    def get_hand_value(self):
        '''Returns the value of hand, points conversion for Ace (from 11 to 1) is done if the value is over 21'''
        value = 0
        num_aces = 0
        for card in self.cards:
            value += card.value()
            if card.rank == 'A':
                num_aces += 1

        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1

        return value
    
    def hit(self, card):
        self.add_card(card)

        if self.get_hand_value() > 21:
            return False
        return True
    
    def double_down(self, card):
        self.bet *= 2
        self.hit(card)
        self.has_doubled_down = True
        return False
    
    def __str__(self):
        hand_str = ', '.join(str(card) for card in self.cards)
        return f"{hand_str}:({self.get_hand_value()})"