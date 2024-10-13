from .deck import Deck
from .player import Player
from .dealer import Dealer
import random

class BlackjackGame:
    def __init__(self, num_decks=1, num_players=1):
        self.deck = Deck(num_decks)
        self.main_player = Player(name="Gracz 1")
        self.bot_players = [Player(name=f"Bot {i+1}") for i in range(num_players - 1)]
        self.dealer = Dealer()

    def start_new_round(self):
        """Rozpoczyna nową rundę gry."""
        self.main_player.reset_hand()
        for bot in self.bot_players:
            bot.reset_hand()
        self.dealer.reset_hand()

        # Rozdanie dwóch kart graczom i krupierowi
        self.main_player.add_card(self.deck.deal_card())
        self.main_player.add_card(self.deck.deal_card())
        for bot in self.bot_players:
            bot.add_card(self.deck.deal_card())
            bot.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())

        print(f"Karty {self.main_player.name}: {self.main_player}")
        for bot in self.bot_players:
            print(f"Karty {bot.name}: {bot}")
        print(f"Karty Dealera: {self.dealer.hand[0]} i [ukryta]")

    def player_hit(self, player):
        """Gracz dobiera kartę."""
        card = self.deck.deal_card()
        player.add_card(card)
        print(f"{player.name} dobrał kartę: {card}")
        print(f"Karty {player.name}: {player}")

        if player.get_hand_value() > 21:
            print(f"{player.name} przekroczył 21! Przegrywasz.")
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
        dealer_value = self.dealer.get_hand_value()
        results = []

        players = [self.main_player] + self.bot_players
        for player in players:
            player_value = player.get_hand_value()
            if player_value > 21:
                results.append(f"{player.name}: Dealer wygrywa!")
            elif dealer_value > 21:
                results.append(f"{player.name}: {player.name} wygrywa!")
            elif player_value > dealer_value:
                results.append(f"{player.name}: {player.name} wygrywa!")
            elif dealer_value > player_value:
                results.append(f"{player.name}: Dealer wygrywa!")
            else:
                results.append(f"{player.name}: Remis!")

        return results

    def play(self):
        """Rozgrywa jedną pełną grę."""
        self.start_new_round()

        # Main player turn
        while True:
            action = input("Chcesz dobrać kartę? (hit/stand): ").lower()
            if action == 'hit':
                if not self.player_hit(self.main_player):
                    break
            elif action == 'stand':
                break
            else:
                print("Nieprawidłowa opcja. Wpisz 'hit' lub 'stand'.")

        # Bot players turn
        for bot in self.bot_players:
            while True:
                action = random.choice(['hit', 'stand'])
                print(f"{bot.name} wybiera: {action}")
                if action == 'hit':
                    if not self.player_hit(bot):
                        break
                elif action == 'stand':
                    break

        if all(player.get_hand_value() <= 21 for player in [self.main_player] + self.bot_players):
            self.dealer_turn()

        results = self.check_winner()
        for result in results:
            print(result)