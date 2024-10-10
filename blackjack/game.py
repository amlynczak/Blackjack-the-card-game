from deck import Deck
from player import Player
from dealer import Dealer

class BlackjackGame:
    def __init__(self, num_decks=1):
        self.deck = Deck(num_decks)
        self.player = Player(name="Gracz")
        self.dealer = Dealer()

    def start_new_round(self):
        """Rozpoczyna nową rundę gry."""
        self.player.reset_hand()
        self.dealer.reset_hand()

        # Rozdanie dwóch kart graczowi i krupierowi
        self.player.add_card(self.deck.deal_card())
        self.player.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())

        print(f"Karty Gracza: {self.player}")
        print(f"Karty Dealera: {self.dealer.hand[0]} i [ukryta]")

    def player_hit(self):
        """Gracz dobiera kartę."""
        card = self.deck.deal_card()
        self.player.add_card(card)
        print(f"Gracz dobrał kartę: {card}")
        print(f"Karty Gracza: {self.player}")

        if self.player.get_hand_value() > 21:
            print("Gracz przekroczył 21! Przegrywasz.")
            return False
        return True

    def dealer_turn(self):
        """Tura krupiera - dealer dobiera karty zgodnie z zasadami."""
        print(f"Karty Dealera: {self.dealer}")
        while self.dealer.should_hit():
            card = self.deck.deal_card()
            self.dealer.add_card(card)
            print(f"Dealer dobrał kartę: {card}")
        print(f"Ręka Dealera: {self.dealer}")

    def check_winner(self):
        """Sprawdza, kto wygrał rundę."""
        player_value = self.player.get_hand_value()
        dealer_value = self.dealer.get_hand_value()

        if player_value > 21:
            return "Dealer wygrywa!"
        elif dealer_value > 21:
            return "Gracz wygrywa!"
        elif player_value > dealer_value:
            return "Gracz wygrywa!"
        elif dealer_value > player_value:
            return "Dealer wygrywa!"
        else:
            return "Remis!"

    def play(self):
        """Rozgrywa jedną pełną grę."""
        self.start_new_round()

        while self.player_hit():
            action = input("Chcesz dobrać kartę? (hit/stand): ").lower()
            if action == 'stand':
                break

        if self.player.get_hand_value() <= 21:
            self.dealer_turn()

        print(self.check_winner())
