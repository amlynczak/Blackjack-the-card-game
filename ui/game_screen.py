import pygame
import sys
import random
import time

from blackjack.card import Card
from blackjack.deck import Deck
from blackjack.player import Player
from blackjack.dealer import Dealer
from blackjack.bot import Bot

from ui.utils import draw_text, draw_button, display_game_state

pygame.init()

SCREEEN_WIDTH = 1000
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
CARD_WIDTH, CARD_HEIGHT = 60, 90

screen = pygame.display.set_mode((SCREEEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

card_images = {}
card_images['back'] = pygame.transform.scale(pygame.image.load("assets/images/cards/back.jpg"), (CARD_WIDTH, CARD_HEIGHT))
for suit in ['spades', 'hearts', 'diamonds', 'clubs']:
    for value in range(2, 11):
        card_images[f"{value}_of_{suit}"] = pygame.transform.scale(pygame.image.load(f"assets/images/cards/{value}_of_{suit}.png"), (CARD_WIDTH, CARD_HEIGHT))
    for face in ['J', 'Q', 'K', 'A']:
        card_images[f"{face}_of_{suit}"] = pygame.transform.scale(pygame.image.load(f"assets/images/cards/{face}_of_{suit}.png"), (CARD_WIDTH, CARD_HEIGHT))

class BlackjackGame:
    def __init__(self, number_of_decks = 1, number_of_players = 4, standard_bet = 20) -> None:
        self.deck = Deck(number_of_decks)
        self.standard_bet = standard_bet
        self.main_player = Player(name="Player", money = 200)
        self.bot_players = [Bot(name=f"Bot {i+1}", money = 60) for i in range(number_of_players - 1)]
        self.dealer = Dealer()
        self.font = pygame.font.Font(None, 36)

    def start_new_round(self):
        if self.main_player.can_play(self.standard_bet):
            self.main_player.reset_hand(self.standard_bet)
        else:
            print("You don't have enough money to play. Game over.")
            exit()
            
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
                display_game_state(screen, self.main_player, self.dealer, self.bot_players, card_images, self.font)
                action = self.get_player_action()
                if action == 'hit':
                    if not self.main_player.hit(self.deck.deal_card(), self.main_player.hand_id):
                        break
                elif action == 'double':
                    if self.main_player.can_double_down():
                        if not self.main_player.double_down(self.deck.deal_card(), self.main_player.hand_id):
                            break
                elif action == 'split':
                    if self.main_player.can_split():
                        self.main_player.split(self.deck.deal_card(), self.deck.deal_card())
                elif action == 'insurance':
                    if self.main_player.can_insurance(self.dealer.hand):
                        self.main_player.insurance(self.dealer.hand)
                elif action == 'surrender':
                    if self.main_player.can_surrender():
                        self.main_player.surrender()
                        break
                elif action == 'stand':
                    break
            self.main_player.hand_id += 1

        # Bot players turn
        for bot in self.bot_players:
            while bot.hand_id < len(bot.hands):
                while True and bot.hands[bot.hand_id].isBlackjack == False:
                    action = bot.decide_action(self.dealer.hand)
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
                    display_game_state(screen, self.main_player, self.dealer, self.bot_players, card_images, self.font)
                    time.sleep(5)
                bot.hand_id += 1

        self.dealer.dealers_turn(self.deck, screen, self.main_player, self.bot_players, card_images, self.font)

        results = self.check_winner()
        for result in results:
            print(result)

        print(f"AGH-coins balance for {self.main_player.name}: {self.main_player.money}")
        for bot in self.bot_players:
            if bot.money == 0:
                print(f"{bot.name} is out of money.")
                self.bot_players.remove(bot)
            else:
                print(f"AGH-coins balance for {bot.name}: {bot.money}")   

    def get_player_action(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        return 'hit'
                    elif event.key == pygame.K_d:
                        return 'double'
                    elif event.key == pygame.K_s:
                        return 'split'
                    elif event.key == pygame.K_i:
                        return 'insurance'
                    elif event.key == pygame.K_u:
                        return 'surrender'
                    elif event.key == pygame.K_t:
                        return 'stand'