import pygame
import sys
import os
import random
import time
import json

from blackjack.card import Card
from blackjack.deck import Deck
from blackjack.player import Player
from blackjack.dealer import Dealer
from blackjack.bot import Bot

from card_counter.counting_bot import CountingBot

from ui.utils import draw_text, draw_button, display_game_state, draw_background, draw_text_center, draw_title

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)

pygame.display.set_caption("Blackjack")        

class BlackjackGame:
    def __init__(self, number_of_decks = 1, number_of_players = 1, counting_prohibited = True, standard_bet = 20):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.deck = Deck(number_of_decks)
        self.counting_prohibited = counting_prohibited
        self.standard_bet = standard_bet
        self.main_player = Player(name="Gracz", money = 1000)
        with open("assets/random_names") as f:
            random_names = f.read().splitlines()
            random.shuffle(random_names)
        if self.counting_prohibited:
            self.bot_players = [Bot(name=random_names[i], money = 200) for i in range(number_of_players - 1)]
        else:
            self.bot_players = [CountingBot(name=random_names[i], money = 150, number_of_decks=number_of_decks) for i in range(number_of_players - 1)]
        self.dealer = Dealer()
        self.players_turn = len(self.bot_players)//2

    def start_new_round(self):
        while True:
            draw_background(self.screen, self.counting_prohibited, True)
            draw_text_center(f"Twoje saldo: {self.main_player.money} WFiIS żetonów", WHITE, self.screen, 200)
            draw_text_center("Jaką stawkę chcesz postawić?", WHITE, self.screen, 250)
            bet_amounts = [10, 20, 50, 100, 200, 500]
            x = 175
            for amount in bet_amounts:
                draw_button(f"{amount}", WHITE, self.screen, x, 350, 100, 50)
                x += 150
            draw_button("Opuść stół", WHITE, self.screen, 500, 450, 200, 50)
            pygame.display.flip()
            bet = None
            while bet is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        for i, amount in enumerate(bet_amounts):
                            if x > 175 + i * 150 and x < 375 + i * 150 and y > 350 and y < 400:
                                bet = amount
                        if x > 500 and x < 700 and y > 450 and y < 500:
                            bet = 'leave'
            if bet == 'leave':
                return False
            elif self.main_player.can_play(bet):
                self.main_player.reset_hand(bet)
                break
            else:
                print("Nie masz wystarczająco żetonów na koncie.")
            
        for bot in self.bot_players[:]:
            if bot.can_play(self.standard_bet):
                bet = bot.decide_bet(self.standard_bet)
                bot.reset_hand(bet)
            else:
                print(f"{bot.name} nie ma wystarczająco żetonów na koncie.")
                self.bot_players.remove(bot)

        self.dealer.reset_hand()

        for i in range(2):
            for bot in self.bot_players[:self.players_turn]:
                if (self.counting_prohibited):
                    bot.add_card(self.deck.deal_card())
                else:
                    bot.add_card(self.deck.deal_card_and_update_counts(self.bot_players+ [self.main_player]))

            if (self.counting_prohibited):
                self.main_player.add_card(self.deck.deal_card())
            else:
                self.main_player.add_card(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]))
            
            for bot in self.bot_players[self.players_turn: len(self.bot_players)]:
                if (self.counting_prohibited):
                    bot.add_card(self.deck.deal_card())
                else:
                    bot.add_card(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]))

            if (not self.counting_prohibited and i == 0):
                self.dealer.add_card(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]))        
            else:
                self.dealer.add_card(self.deck.deal_card())
                
            
        if self.main_player.get_hand_value() == 21:
            print("♣♦♥♠ Blackjack! ♣♦♥♠")
            self.main_player.hands[self.main_player.hand_id].isBlackjack = True
            print(f"{self.main_player} Blackjack!")
        else:
            print(f"{self.main_player}")

        for bot in self.bot_players[:]:
            if bot.get_hand_value() == 21:
                bot.hands[bot.hand_id].isBlackjack = True
                print(f"{bot} Blackjack!")
            else:
                print(f"{bot}")
        
        print(f"Dealer: {self.dealer.hand[0]} and one [hidden] card")

        display_game_state(self.screen, self.main_player, self.dealer, self.bot_players, self.counting_prohibited)

        return True

    def check_winner(self):
        dealer_value = self.dealer.get_hand_value()
        results = []
        players = [self.main_player] + self.bot_players

        for player in players:
            for hand in player.hands:
                if player.has_surrenderred:
                    results.append(f"{hand.name} poddał się")
                    continue
                if hand.isBlackjack:
                    if dealer_value == 21 and len(self.dealer.hand) == 2:
                        results.append(f"{hand.name}: remis")
                        player.money += hand.bet
                    else:
                        results.append(f"{hand.name} wygrał - Blackjack!")
                        player.money += hand.bet * 2.5
                    continue
                hand_value = hand.get_hand_value()
                if hand_value > 21:
                    results.append(f"{hand.name}: Dealer wygrał!")
                elif dealer_value > 21:
                    results.append(f"{hand.name} wygrał!")
                    player.money += hand.bet * 2
                elif hand_value == 21 and dealer_value == 21 and len(self.dealer.hand) == 2:
                    results.append(f"{hand.name}: Dealer wygrał!")
                elif hand_value > dealer_value:
                    results.append(f"{hand.name} wygrał!")
                    player.money += hand.bet * 2
                elif dealer_value > hand_value:
                    results.append(f"{hand.name}: Dealer wygrał!")
                else:
                    results.append(f"{hand.name}: remis")
                    player.money += hand.bet

            if dealer_value == 21 and len(self.dealer.hand) == 2 and player.is_insured:
                results.append(f"{player.name}: Ubezpieczenie zadziałało!")
                player.money += player.insurance_bet * 2
            elif dealer_value != 21 and len(self.dealer.hand) == 2 and player.is_insured:
                results.append(f"{player.name}: Ubezpieczenie stracone")
            
        draw_background(self.screen, self.counting_prohibited, True)
        draw_title("Wyniki rundy", WHITE, self.screen, 50)
        y = 100
        for result in results:
            draw_text_center(result, WHITE, self.screen, y)
            y += 50
        pygame.display.flip()
        time.sleep(5)
        return results
    
    def play_round(self):
        """Plays a game of blackjack"""
        play_on = self.start_new_round()
        if not play_on:
            return False
        
        for bot in self.bot_players[:self.players_turn]:
            while bot.hand_id < len(bot.hands):
                increment = True
                while True and bot.hands[bot.hand_id].isBlackjack == False:
                    increment = True
                    display_game_state(self.screen, self.main_player, self.dealer, self.bot_players, self.counting_prohibited)
                    time.sleep(1)
                    action = bot.decide_final_action(self.dealer.hand)
                    if action == 'hit' and bot.can_hit(bot.hand_id):
                        print(f"{bot.name} hits")
                        if self.counting_prohibited and not bot.hit(self.deck.deal_card(), bot.hand_id):
                            break
                        elif not self.counting_prohibited and not bot.hit(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]), bot.hand_id):
                            break
                    elif action == 'double' and bot.can_double_down(bot.hand_id):
                        print(f"{bot.name} doubles down")
                        if self.counting_prohibited and not bot.double_down(self.deck.deal_card(), bot.hand_id):
                            break
                        elif not self.counting_prohibited and not bot.double_down(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]), bot.hand_id):
                            break
                    elif action == 'split' and bot.can_split():
                        print(f"{bot.name} splits")
                        if self.counting_prohibited:
                            bot.split(self.deck.deal_card(), self.deck.deal_card())
                            increment = False
                        else:
                            bot.split(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]), self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]))
                            increment = False
                    elif action == 'stand' and bot.can_stand(bot.hand_id):
                        print(f"{bot.name} stands")
                        display_game_state(self.screen, self.main_player, self.dealer, self.bot_players, self.counting_prohibited)
                        break
                    elif action == 'surrender' and bot.can_surrender():
                        bot.surrender()
                        break
                    elif action == 'insurance' and bot.can_insurance(self.dealer.hand):
                        bot.insurance(self.dealer.hand)
                if increment:
                    bot.hand_id += 1
        
        print("player's turn")
        while self.main_player.hand_id < len(self.main_player.hands):
            increment = True
            while True and self.main_player.hands[self.main_player.hand_id].isBlackjack == False:
                increment = True
                display_game_state(self.screen, self.main_player, self.dealer, self.bot_players, self.counting_prohibited, players_turn=True)
                action = self.get_player_action()
                if self.main_player.hands[self.main_player.hand_id].get_hand_value() > 21:
                    break
                else:
                    if action == 'hit' and self.main_player.can_hit(self.main_player.hand_id):
                        print("HIT")
                        if self.counting_prohibited and not self.main_player.hit(self.deck.deal_card(), self.main_player.hand_id):
                            break
                        elif not self.counting_prohibited and not self.main_player.hit(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]), self.main_player.hand_id):
                            break
                    elif action == 'double' and self.main_player.can_double_down(self.main_player.hand_id):
                        print("DOUBLE DOWN")
                        if self.counting_prohibited and not self.main_player.double_down(self.deck.deal_card(), self.main_player.hand_id):
                            break
                        elif not self.counting_prohibited and not self.main_player.double_down(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]), self.main_player.hand_id):
                            break
                    elif action == 'split' and self.main_player.can_split():
                        print("SPLIT")
                        if self.counting_prohibited:
                            self.main_player.split(self.deck.deal_card(), self.deck.deal_card())
                            increment = False
                            break
                        else:
                            self.main_player.split(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]), self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]))
                            increment = False
                            break
                    elif action == 'insurance' and self.main_player.can_insurance(self.dealer.hand):
                        self.main_player.insurance(self.dealer.hand)
                    elif action == 'surrender' and self.main_player.can_surrender():
                        self.main_player.surrender()
                        break
                    elif action == 'stand' and self.main_player.can_stand(self.main_player.hand_id):
                        print("STAND")
                        display_game_state(self.screen, self.main_player, self.dealer, self.bot_players, self.counting_prohibited, players_turn=True)
                        break
            if increment:
                self.main_player.hand_id += 1

        for bot in self.bot_players[self.players_turn:]:
            while bot.hand_id < len(bot.hands):
                increment = True
                while True and bot.hands[bot.hand_id].isBlackjack == False:
                    increment = True
                    display_game_state(self.screen, self.main_player, self.dealer, self.bot_players, self.counting_prohibited)
                    time.sleep(1)
                    action = bot.decide_final_action(self.dealer.hand)
                    if action == 'hit' and bot.can_hit(bot.hand_id):
                        print(f"{bot.name} hits")
                        if self.counting_prohibited and not bot.hit(self.deck.deal_card(), bot.hand_id):
                            break
                        elif not self.counting_prohibited and not bot.hit(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]), bot.hand_id):
                            break
                    elif action == 'double' and bot.can_double_down(bot.hand_id):
                        print(f"{bot.name} doubles down")
                        if self.counting_prohibited and not bot.double_down(self.deck.deal_card(), bot.hand_id):
                            break
                        elif not self.counting_prohibited and not bot.double_down(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]), bot.hand_id):
                            break
                    elif action == 'split' and bot.can_split():
                        print(f"{bot.name} splits")
                        if self.counting_prohibited:
                            bot.split(self.deck.deal_card(), self.deck.deal_card())
                            increment = False
                        else:
                            bot.split(self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]), self.deck.deal_card_and_update_counts(self.bot_players + [self.main_player]))
                            increment = False
                    elif action == 'stand' and bot.can_stand(bot.hand_id):
                        print(f"{bot.name} stands")
                        display_game_state(self.screen, self.main_player, self.dealer, self.bot_players, self.counting_prohibited)
                        break
                    elif action == 'surrender' and bot.can_surrender():
                        bot.surrender()
                        break
                    elif action == 'insurance' and bot.can_insurance(self.dealer.hand):
                        bot.insurance(self.dealer.hand)
                if increment:
                    bot.hand_id += 1

        display_game_state(self.screen, self.main_player, self.dealer, self.bot_players, self.counting_prohibited, dealer_show_all=True)
        for players in [self.main_player] + self.bot_players:
            players.update_count(self.dealer.hand[1])
        self.dealer.dealers_turn(self.deck, self.screen, self.main_player, self.bot_players, self.counting_prohibited)
        time.sleep(5)

        results = self.check_winner()
        for result in results:
            print(result)

        print(f"AGH-coins balance for {self.main_player.name}: {self.main_player.money}")
        for bot in self.bot_players[:]:
            if bot.money == 0:
                print(f"{bot.name} is out of money.")
                self.bot_players.remove(bot)
                self.players_turn = len(self.bot_players)//2
            else:
                print(f"AGH-coins balance for {bot.name}: {bot.money}")  

        return True

    def play(self):
        play_on = True
        while play_on:
            play_on = self.play_round()

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
                    elif event.key == pygame.K_p:
                        return 'split'
                    elif event.key == pygame.K_i:
                        return 'insurance'
                    elif event.key == pygame.K_u:
                        return 'surrender'
                    elif event.key == pygame.K_s:
                        return 'stand'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if x > 20 and x < 120 and y > SCREEN_HEIGHT - 120 and y < SCREEN_HEIGHT - 70:
                        print("HIT")
                        return 'hit'
                    elif x > 20 and x < 120 and y > SCREEN_HEIGHT - 60 and y < SCREEN_HEIGHT - 10:
                        print("STAND")
                        return 'stand'
                    elif x > 130 and x < 230 and y > SCREEN_HEIGHT - 120 and y < SCREEN_HEIGHT - 70:
                        print("DOUBLE DOWN")
                        return 'double'
                    elif x > 130 and x < 230 and y > SCREEN_HEIGHT - 60 and y < SCREEN_HEIGHT - 10:
                        print("SPLIT")
                        return 'split'
                    elif x > 240 and x < 340 and y > SCREEN_HEIGHT - 120 and y < SCREEN_HEIGHT - 70:
                        return 'insurance'
                    elif x > 240 and x < 340 and y > SCREEN_HEIGHT - 60 and y < SCREEN_HEIGHT - 10:
                        return 'surrender'
