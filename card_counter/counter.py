from abc import ABC, abstractmethod

class Counter(ABC):
    def __init__(self, num_decks):
        self.running_count = 0
        self.cards_dealt = 0
        self.num_decks = num_decks
        self.true_count = 0

    def reset(self):
        self.running_count = 0
        self.cards_dealt = 0
        self.true_count = 0

    def update_count(self, card):
        self.running_count += self.card_value(card)
        self.cards_dealt += 1
        if self.num_decks * 52 <= self.cards_dealt:
            self.reset()
        self.update_true_count()

    def update_true_count(self):
        decks_remaining = max(self.num_decks - round(self.cards_dealt / 52), 1)
        self.true_count = self.running_count // decks_remaining

    def get_running_count(self):
        return self.running_count
    
    def get_count(self):
        return self.true_count
    
    @abstractmethod
    def card_value(self, card):
        pass