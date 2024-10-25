from .deck import Deck
from .player import Player
from .dealer import Dealer
from .bot import Bot
import time

class BlackjackGame:
    def __init__(self, num_decks=1, num_players=1, standard_bet=20):
        '''Initializes the game with a number of decks and players'''
        self.deck = Deck(num_decks)
        self.standard_bet = standard_bet
        self.main_player = Player(name="Player", money = 200)
        self.bot_players = [Bot(name=f"Bot {i+1}", money = 200) for i in range(num_players - 1)]
        self.dealer = Dealer()

    def start_new_round(self):
        """start for a new round"""
        if self.main_player.can_play(self.standard_bet):
            self.main_player.reset_hand(self.standard_bet)
        else:
            print("You don't have enough money to play. Game over.")
            return
            
        for bot in self.bot_players:
            if bot.can_play(self.standard_bet):
                bot.reset_hand(self.standard_bet)
            else:
                print(f"{bot.name} doesn't have enough money to play.")
                self.bot_players.remove(bot)

        self.dealer.reset_hand()

        #deal cards
        self.main_player.add_card(self.deck.deal_card())
        self.main_player.add_card(self.deck.deal_card())

        for bot in self.bot_players:
            bot.add_card(self.deck.deal_card())
            bot.add_card(self.deck.deal_card())
        
        self.dealer.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())

        if self.main_player.get_hand_value() == 21:
            print("♣♦♥♠ Blackjack! ♣♦♥♠")
            time.sleep(5)
            self.main_player.hands[self.main_player.hand_id].isBlackjack = True
            print(f"{self.main_player} Blackjack!")
        else:
            print(f"{self.main_player}")

        for bot in self.bot_players:
            if bot.get_hand_value() == 21:
                bot.hands[bot.hand_id].isBlackjack = True
                print(f"{bot} Blackjack!")
            else:
                print(f"{bot}")
        
        print(f"Dealer: {self.dealer.hand[0]} and one [hidden] card")

    def check_winner(self):
        '''Checks the winner of the game'''
        dealer_value = self.dealer.get_hand_value()
        results = []

        players = [self.main_player] + self.bot_players
        for player in players:
            for hand in player.hands:
                if player.has_surrenderred:
                    results.append(f"{hand.name}: Surrendered!")
                    continue
                if hand.isBlackjack:
                    if dealer_value == 21 and len(self.dealer.hand) == 2:
                        results.append(f"{hand.name}: Draw!")
                        player.money += hand.bet
                    else:
                        results.append(f"{hand.name} won!")
                        player.money += hand.bet * 2.5
                    continue
                hand_value = hand.get_hand_value()
                if hand_value > 21:
                    results.append(f"{hand.name}: Dealer won!")
                elif dealer_value > 21:
                    results.append(f"{hand.name} won!")
                    player.money += hand.bet * 2
                elif hand_value == 21 and dealer_value == 21 and len(self.dealer.hand) == 2:
                    results.append(f"{hand.name}: Dealer won!")
                elif hand_value > dealer_value:
                    results.append(f"{hand.name} won!")
                    player.money += hand.bet * 2
                elif dealer_value > hand_value:
                    results.append(f"{hand.name}: Dealer won!")
                else:
                    results.append(f"{hand.name}: Draw!")
                    player.money += hand.bet

            if dealer_value == 21 and len(self.dealer.hand) == 2 and player.isInsured:
                if player.isInsured:
                    results.append(f"{player.name}: Insurance won!")
                    player.money += player.insurance_bet * 2
                else:
                    results.append(f"{player.name}: Insurance lost!") 

        return results

    def play(self):
        """Plays a game of blackjack"""
        self.start_new_round()
        
        # Main player turn
        while self.main_player.hand_id < len(self.main_player.hands):
            while True and self.main_player.hands[self.main_player.hand_id].isBlackjack == False:
                print(f"\n{self.main_player}")
                action = input("What's your action (hit/double/split/stand/insurance/surrender): ").lower()
                if action == 'hit':
                    if not self.main_player.hit(self.deck.deal_card(), self.main_player.hand_id):
                        break
                elif action == 'double':
                    if self.main_player.can_double_down():
                        if not self.main_player.double_down(self.deck.deal_card(), self.main_player.hand_id):
                            break
                    else:
                        print("You can't double down. (You can only double down if you have two cards). Try again with a different action.")
                elif action == 'split':
                    if self.main_player.can_split():
                        self.main_player.split(self.deck.deal_card(), self.deck.deal_card())
                    else:
                        print("You can't split these cards. (You can only split if you have two cards of the same rank). Try again with a different action.")
                elif action == 'insurance':
                    if self.main_player.can_insurance(self.dealer.hand):
                        self.main_player.insurance(self.dealer.hand)
                    else:
                        print("You can't take insurance. (Dealer's card is not an Ace or you're already insured). Try again with a different action.")
                elif action == 'surrender':
                    if self.main_player.can_surrender():
                        self.main_player.surrender()
                        break
                    else:
                        print("You can't surrender. (You can do it only on first two cards). Try again with a different action.")
                elif action == 'stand':
                    break
                else:
                    print("Invalid action. Try again.")
            self.main_player.hand_id += 1

        # Bot players turn
        for bot in self.bot_players:
            while bot.hand_id < len(bot.hands):
                while True and bot.hands[bot.hand_id].isBlackjack == False:
                    print(f"\n{bot}")
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