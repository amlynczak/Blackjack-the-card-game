'''
Class representing a card in a deck of cards
'''
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank}_of_{self.suit}"
    
    def value(self):
        '''Returns the value of the card; the value of Ace is 11, 
        conversion into 1 is done while calculating the hand value'''
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)
        