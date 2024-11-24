from abc import ABC, abstractmethod

class Counter(ABC):
    def __init__(self):
        self.running_count = 0
        self.cards_dealt = 0
        self.true_count = 0

    def reset(self):
        self.running_count = 0
        self.cards_dealt = 0
        self.true_count = 0

    def update_count(self, card, num_decks):
        self.running_count += self.card_value(card)
        self.cards_dealt += 1
        self.update_true_count(num_decks)

    def update_true_count(self, num_decks):
        decks_remaining = num_decks - round(self.cards_dealt / 52)
        self.true_count = self.running_count // decks_remaining

    def get_count(self):
        return self.true_count
    
    @abstractmethod
    def card_value(self, card):
        pass