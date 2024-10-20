from .deck import Deck
from .player import Player
from .dealer import Dealer
from .bot import Bot

class BlackjackGame:
    def __init__(self, num_decks=1, num_players=1):
        '''Initializes the game with a number of decks and players'''
        self.deck = Deck(num_decks)
        self.main_player = Player(name="Player")
        self.bot_players = [Bot(name=f"Bot {i+1}") for i in range(num_players - 1)]
        self.dealer = Dealer()

    def start_new_round(self):
        """start for a new round"""
        self.main_player.reset_hand()
        for bot in self.bot_players:
            bot.reset_hand()
        self.dealer.reset_hand()

        #deal cards
        self.main_player.add_card(self.deck.deal_card(), 0)
        self.main_player.add_card(self.deck.deal_card(), 0)
        for bot in self.bot_players:
            bot.add_card(self.deck.deal_card())
            bot.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())

        print(f"{self.main_player}")
        for bot in self.bot_players:
            print(f"{bot}")
        print(f"Dealer: {self.dealer.hand[0]} and one [hidden] card")

    def check_winner(self):
        '''Checks the winner of the game'''
        dealer_value = self.dealer.get_hand_value()
        results = []

        players = [self.main_player] + self.bot_players
        for player in players:
            for hand in player.hands:
                hand_value = hand.get_hand_value()
                if hand_value > 21:
                    results.append(f"{hand.name}: Dealer won!")
                elif dealer_value > 21:
                    results.append(f"{player.name}: {hand.name} won!")
                    player.money += hand.bet * 2
                elif hand_value > dealer_value:
                    results.append(f"{player.name}: {hand.name} won!")
                    player.money += hand.bet * 2
                elif dealer_value > hand_value:
                    results.append(f"{hand.name}: Dealer won!")
                else:
                    results.append(f"{hand.name}: Draw!")
                    player.money += hand.bet

        return results

    def play(self):
        """Plays a game of blackjack"""
        self.start_new_round()
        
        # Main player turn
        while self.main_player.hand_id < len(self.main_player.hands):
            while True:
                action = input("What's your action (hit/double/split/stand): ").lower()
                if action == 'hit':
                    if not self.main_player.hit(self.deck.deal_card()):
                        break
                elif action == 'double':
                    if self.main_player.can_double_down():
                        if not self.main_player.double_down(self.deck.deal_card()):
                            break
                    else:
                        print("You can't double down. Try again with a different action.")
                elif action == 'split':
                    if self.main_player.can_split():
                        self.main_player.split(self.deck.deal_card(), self.deck.deal_card())
                    else:
                        print("You can't split these cards. Try again with a different action.")
                elif action == 'stand':
                    break
                else:
                    print("Invalid action. Try again.")
            self.main_player.hand_id += 1

        # Bot players turn
        for bot in self.bot_players:
            while bot.hand_id < len(bot.hands):
                while True:
                    action = bot.decide_action(self.dealer.hand)
                    print(f"{bot.name} choose to: {action}")
                    if action == 'hit':
                        if not bot.hit(self.deck.deal_card()):
                            break
                    elif action == 'double':
                        if not bot.double_down(self.deck.deal_card()):
                            break
                    elif action == 'split':
                        if bot.can_split():
                            bot.split(self.deck.deal_card(), self.deck.deal_card())
                    elif action == 'stand':
                        break
                bot.hand_id += 1

        self.dealer.dealers_turn(self.deck)

        results = self.check_winner()
        for result in results:
            print(result)

        print(f"AGH-coins balance for {self.main_player.name}: {self.main_player.money}")
        for bot in self.bot_players:
            print(f"AGH-coins balance for {bot.name}: {bot.money}")