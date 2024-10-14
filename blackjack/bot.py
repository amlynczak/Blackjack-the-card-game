from .player import Player
import random

class Bot(Player):
    def __init__(self, name="Bot"):
        super().__init__(name)

    def decide_action(self):
        """Decides whether to hit or stand based on the current hand value."""
        hand_value = self.get_hand_value()
        if hand_value < 17:
            return 'hit'
        else:
            return 'stand'