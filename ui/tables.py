import pygame
import sys
import os
import json

from ui.utils import draw_button, draw_text
from ui.game_screen import BlackjackGame

os.environ['SDL_VIDEO_CENTERED'] = '1'

GREEN = (0, 128, 0)
DARK_GREEN = (0, 100, 0)
WHITE = (255, 255, 255)

def choose_table(screen):
    screen.fill((0, 0, 0))
    pygame.display.set_caption("Wybierz stół")

    clock = pygame.time.Clock()

    rect1 = pygame.Rect(100, 100, 250, 250)
    rect2 = pygame.Rect(450, 100, 250, 250)
    back_button_rect = pygame.Rect(300, 500, 200, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect1.collidepoint(event.pos):
                    num_of_players = json.loads(open("assets/settings.json").read())["number_of_players"]
                    num_of_decks = json.loads(open("assets/settings.json").read())["number_of_decks"]
                    pygame.display.set_caption("♣♦♥♠ Blackjack - Stół 1 ♣♦♥♠")
                    game = BlackjackGame(number_of_players=num_of_players, number_of_decks=num_of_decks)
                    game.play()
                    screen = pygame.display.set_mode((800, 600))
                    screen.fill((0, 0, 0))
                    pygame.display.set_caption("Wybierz stół")
                elif rect2.collidepoint(event.pos):
                    num_of_players = json.loads(open("assets/settings.json").read())["number_of_players"]
                    num_of_decks = json.loads(open("assets/settings.json").read())["number_of_decks"]
                    pygame.display.set_caption("♣♦♥♠ Blackjack - Stół 2 ♣♦♥♠")
                    game = BlackjackGame(number_of_players=num_of_players, number_of_decks=num_of_decks, counting_prohibited=False)
                    game.play()
                    screen = pygame.display.set_mode((800, 600))
                    screen.fill((0, 0, 0))
                    pygame.display.set_caption("Wybierz stół")
                elif back_button_rect.collidepoint(event.pos):
                    pygame.display.set_caption("♣♦♥♠ Blackjack app ♣♦♥♠")
                    return

        pygame.draw.rect(screen, GREEN, rect1)
        draw_text('Stół 1', (255, 255, 255), screen, 150, 50)
        draw_text('Liczenie kart zakazane', (255, 255, 255), screen, 115, 400)
        pygame.draw.rect(screen, DARK_GREEN, rect2)
        draw_text('Stół 2', (255, 255, 255), screen, 500, 50)
        draw_text('Można liczyć karty', (255, 255, 255), screen, 485, 400)

        draw_button('Powrót', WHITE, screen, 300, 500, 200, 50)

        pygame.display.flip()
        clock.tick(60)