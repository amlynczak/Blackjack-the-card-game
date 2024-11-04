import pygame
import sys
import math

GREEN = (0, 128, 0)
WHITE = (255, 255, 255)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_button(text, font, color, surface, x, y, width, height):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, font, (0, 0, 0), surface, x + 10, y + 10)


def display_game_state(screen, main_player, dealer, bot_players, card_images, card_images_bots, font, dealer_show_all=False):
        screen.fill(GREEN)
        for i, hand in enumerate(main_player.hands):
            display_hand(hand, screen.get_width()//2 - 50 + i * 30, screen.get_height() - 200, screen, card_images, font)
        shift = 30 + 50 * (dealer.hand.__len__() - 1)
        display_hand_dealer(dealer, screen.get_width()//2 - shift , 20, screen, card_images, font, dealer_show_all)

        num_of_bots = len(bot_players)
        angle_step = 180 // 7
        radius = 300
        center_x_num_less_4 = screen.get_width() // 2 + 100
        center_x_num_more_4 = screen.get_width() // 2 - 100
        center_y = 80

        for i, bot in enumerate(bot_players):
            angle = (i + 1) * angle_step
            if i < 3:
                center_x = center_x_num_less_4
                r_side = True
            else:
                center_x = center_x_num_more_4
                r_side = False
            x = center_x + int(radius * math.cos(math.radians(angle)))
            y = center_y + int(radius * math.sin(math.radians(angle)))
            for hand in bot.hands:
                if r_side:
                    display_hand_bot(hand, x+100, y, screen, card_images_bots, font, r_side)
                else:
                    display_hand_bot(hand, x - 100, y, screen, card_images_bots, font, r_side)
        pygame.display.flip()

def display_hand(hand, x, y, screen, card_images, font):
    for j, card in enumerate(hand.cards):
        screen.blit(card_images[str(card)], (x + j * 100, y))
    text = font.render(f"{hand.name}: {hand.get_hand_value()}", True, WHITE)
    screen.blit(text, (x, y + 100))
    if hand.isBlackjack:
        text = font.render("Blackjack!", True, WHITE)
        screen.blit(text, (x + 200, y + 100))

def display_hand_bot(hand, x, y, screen, card_images, font, right_hand_side=True):
    for j, card in enumerate(hand.cards):
        if right_hand_side:
            screen.blit(card_images[str(card)], (x - j * 20, y - j * 20))
        else:
            screen.blit(card_images[str(card)], (x + j * 20, y - j * 20))
    text = font.render(f"{hand.get_hand_value()}", True, WHITE)
    screen.blit(text, (x, y + 100))
    #if hand.isBlackjack:
    #   text = font.render("Blackjack!", True, WHITE)
    #   screen.blit(text, (x + 200, y + 100))

def display_hand_dealer(dealer, x, y, screen, card_images, font, show_all=False):
    for i, card in enumerate(dealer.hand):
        if i == 0:
            screen.blit(card_images[str(card)], (x + i * 100, y))
        elif show_all:
            screen.blit(card_images[str(card)], (x + i * 100, y))
        else:
            screen.blit(card_images['back'], (x + i * 100, y))
    
    if not show_all:
        text = font.render(f"Dealer: {dealer.hand[0]} and [hidden]", True, WHITE)
    else:
        text = font.render(f"Dealer: (Points: {dealer.get_hand_value()})", True, WHITE)
    screen.blit(text, (x, y + 100))