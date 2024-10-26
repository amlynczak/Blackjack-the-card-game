import pygame
import sys
from blackjack.game import BlackjackGame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (34, 139, 34)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("♣♦♥♠ Blackjack game ♣♦♥♠")
card_back = pygame.image.load("assets/images/card_back.jpg")

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def start_ui():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 55)

    game = BlackjackGame()
    game.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the background
        screen.fill(BG_COLOR)

        # Draw elements (placeholders)
        screen.blit(card_back, (100, 100))  # Example card position
        draw_text('Blackjack', font, (255, 255, 255), screen, 300, 50)

        draw_text(f'Player Score: {game.player.score}', font, (255, 255, 255), screen, 50, 500)
        draw_text(f'Dealer Score: {game.dealer.score}', font, (255, 255, 255), screen, 600, 500)

        # Update the display
        pygame.display.flip()
        clock.tick(30)
