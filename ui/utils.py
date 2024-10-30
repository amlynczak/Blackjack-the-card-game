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


def display_game_state(screen, main_player, dealer, bot_players, card_images, font, dealer_show_all=False):
        screen.fill(GREEN)
        display_hand(main_player.hands, 100, 500, screen, card_images, font)
        display_hand_dealer(dealer.hand, 100, 50, screen, card_images, font, dealer_show_all)
        for i, bot in enumerate(bot_players):
            display_hand(bot.hands, 500, 200 + i * 150, screen, card_images, font)
        pygame.display.flip()

def display_hand(hands, x, y, screen, card_images, font):
    for i, hand in enumerate(hands):
        for j, card in enumerate(hand.cards):
            screen.blit(card_images[str(card)], (x + j * 100, y + i * 100))
        text = font.render(f"{hand.name}: {hand.get_hand_value()}", True, WHITE)
        screen.blit(text, (x, y + i * 100 + 100))
        if hand.isBlackjack:
            text = font.render("Blackjack!", True, WHITE)
            screen.blit(text, (x + 200, y + i * 100 + 100))

def display_hand_dealer(hand, x, y, screen, card_images, font, show_all=False):
    for i, card in enumerate(hand):
        if i == 0:
            screen.blit(card_images[str(card)], (x + i * 100, y))
        elif show_all:
            screen.blit(card_images[str(card)], (x + i * 100, y))
        else:
            screen.blit(card_images['back'], (x + i * 100, y))
    text = font.render(f"Dealer: {hand[0]}", True, WHITE)
    screen.blit(text, (x, y + 100))