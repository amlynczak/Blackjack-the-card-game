from .deck import Deck
from .player import Player
from .dealer import Dealer
from .bot import Bot

class BlackjackGame:
    def __init__(self, num_decks=1, num_players=1):
        self.deck = Deck(num_decks)
        self.main_player = Player(name="Gracz")
        self.bot_players = [Bot(name=f"Bot {i+1}") for i in range(num_players - 1)]
        self.dealer = Dealer()

    def start_new_round(self):
        """Rozpoczyna nową rundę gry."""
        self.main_player.reset_hand()
        for bot in self.bot_players:
            bot.reset_hand()
        self.dealer.reset_hand()

        # Rozdanie dwóch kart graczom i krupierowi
        self.main_player.add_card(self.deck.deal_card(), 0)
        self.main_player.add_card(self.deck.deal_card(), 0)
        for bot in self.bot_players:
            bot.add_card(self.deck.deal_card())
            bot.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())

        print(f"Karty {self.main_player.name}: {self.main_player}")
        for bot in self.bot_players:
            print(f"Karty {bot.name}: {bot}")
        print(f"Karty Dealera: {self.dealer.hand[0]} i [ukryta]")

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
            action = input("Chcesz dobrać kartę? (hit/stand/double): ").lower()
            if action == 'hit':
                if not self.main_player.hit(self.deck.deal_card()):
                    break
            elif action == 'double':
                if not self.main_player.double_down(self.deck.deal_card()):
                    break
            elif action == 'stand':
                break
            else:
                print("Nieprawidłowa opcja. Wpisz 'hit' lub 'stand'.")

        # Bot players turn
        for bot in self.bot_players:
            while True:
                action = bot.decide_action()
                print(f"{bot.name} wybiera: {action}")
                if action == 'hit':
                    if not bot.hit(self.deck.deal_card()):
                        break
                elif action == 'stand':
                    break

        #if all(player.get_hand_value() <= 21 for player in [self.main_player] + self.bot_players):
        self.dealer.dealers_turn(self.deck)

        results = self.check_winner()
        for result in results:
            print(result)