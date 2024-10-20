class Card:
    def __init__(self, rank, suit):
        '''Initializes the card with a rank and suit'''
        self.rank = rank
        self.suit = suit

    def __str__(self):
        '''Returns a string representation of the card'''
        return f"{self.rank}{self.suit}"
    
    def value(self):
        '''Returns the value of the card'''
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11 #Ace can have value of 1, but we will handle that later
        else:
            return int(self.rank)
        