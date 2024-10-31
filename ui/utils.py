import pygame
import sys

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
            display_hand(hand, 100 + i * 300, 500, screen, card_images, font)
        display_hand_dealer(dealer, 350, 50, screen, card_images, font, dealer_show_all)
        for i, bot in enumerate(bot_players):
            for hand in bot.hands:
                if hand.isBlackjack:
                    print(f"{bot} Blackjack!")
                display_hand_bot(hand, 50 + i*100, 200, screen, card_images_bots, font)
        pygame.display.flip()

def display_hand(hand, x, y, screen, card_images, font):
    for j, card in enumerate(hand.cards):
        screen.blit(card_images[str(card)], (x + j * 100, y))
    text = font.render(f"{hand.name}: {hand.get_hand_value()}", True, WHITE)
    screen.blit(text, (x, y + 100))
    if hand.isBlackjack:
        text = font.render("Blackjack!", True, WHITE)
        screen.blit(text, (x + 200, y + 100))

def display_hand_bot(hand, x, y, screen, card_images, font):
    for j, card in enumerate(hand.cards):
        screen.blit(card_images[str(card)], (x + j * 20, y + j * 20))
    text = font.render(f"{hand.get_hand_value()}", True, WHITE)
    screen.blit(text, (x, y + 100))
    if hand.isBlackjack:
        text = font.render("Blackjack!", True, WHITE)
        screen.blit(text, (x + 200, y + 100))

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