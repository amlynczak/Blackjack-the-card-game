import pygame
import sys

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_button(text, font, color, surface, x, y, width, height):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, font, (0, 0, 0), surface, x + 10, y + 10)


def draw_card(screen, card, x, y):
    if card is not None:
        card_image = pygame.image.load(f'assets/images/cards/{card}.jpg')
        card_image = pygame.transform.scale(card_image, (100, 150))
        screen.blit(card_image, (x, y))
    else:
        card_image = pygame.image.load('assets/images/cards/back.jpg')
        card_image = pygame.transform.scale(card_image, (100, 150))
        screen.blit(card_image, (x, y))