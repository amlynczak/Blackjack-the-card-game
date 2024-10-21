class Hand:
    def __init__(self, hand_name):
        '''Initializes the hand with a name, cards, and bet'''
        self.cards = []
        self.name = hand_name
        self.bet = 20
        self.isBlackjack = False

    def add_card(self, card):
        """Adds a card to the hand."""
        self.cards.append(card)

    def get_hand_value(self):
        """Calculates the value of the hand with aces handled."""
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
        '''Player takes a card from the deck. (for this hand)'''
        self.add_card(card)
        print(f"{card} for {self.name}")
        print(f"{self.name}: {self}")

        if self.get_hand_value() > 21:
            print(f"{self.name} przekroczył 21! Przegrywasz.")
            return False
        return True
    
    def double_down(self, card):
        '''Player doubles down'''
        self.bet *= 2
        self.hit(card)
        return False
    
    def __str__(self):
        '''Returns a string representation of the hand'''
        hand_str = ', '.join(str(card) for card in self.cards)
        return f"{hand_str} (Points: {self.get_hand_value()})"