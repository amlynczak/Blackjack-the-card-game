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

        center_y = 80
        radius = 300

        bots_right_side = bot_players[:len(bot_players)//2]
        right_side_hands = []
        for bot in bots_right_side:
            right_side_hands.extend(bot.hands)
        if len(right_side_hands) != 0:
            angle_step_right = 90 // len(right_side_hands)
            center_x_right_side = screen.get_width() // 2 + 200
            for i, hand in enumerate(right_side_hands):
                angle = (i + 1) * angle_step_right
                x = center_x_right_side + int(radius * math.cos(math.radians(angle)))
                y = center_y + int(radius * math.sin(math.radians(angle)))
                display_hand_bot(hand, x, y, screen, card_images_bots, font, True)

        bots_left_side = bot_players[len(bot_players)//2:]
        left_side_hands = []
        for bot in bots_left_side:
            left_side_hands.extend(bot.hands)
        if len(left_side_hands) != 0:
            angle_step_left = 90 // len(left_side_hands)
            center_x_left_side = screen.get_width() // 2 - 200
            for i, hand in enumerate(left_side_hands):
                angle = i * angle_step_left + 90
                x = center_x_left_side + int(radius * math.cos(math.radians(angle)))
                y = center_y + int(radius * math.sin(math.radians(angle)))
                display_hand_bot(hand, x, y, screen, card_images_bots, font, False)
        
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
        card_img = card_images[str(card)]
        if hand.has_doubled_down and j == 2:
            card_img = pygame.transform.rotate(card_img, 90)
        
        if right_hand_side:
            screen.blit(card_img, (x - j * 20, y - j * 20))
        else:
            screen.blit(card_img, (x + j * 20, y - j * 20))
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