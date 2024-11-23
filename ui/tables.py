import pygame
import sys
import os
import json

from ui.utils import draw_button, draw_text
from ui.game_screen import BlackjackGame

os.environ['SDL_VIDEO_CENTERED'] = '1'

def choose_table(screen):
    screen.fill((0, 0, 0))
    pygame.display.set_caption("Choose table")

    button_font = pygame.font.SysFont(None, 35)
    clock = pygame.time.Clock()

    # Define rectangles
    rect1 = pygame.Rect(100, 100, 250, 250)
    rect2 = pygame.Rect(450, 100, 250, 250)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect1.collidepoint(event.pos):
                    num_of_players = json.loads(open("assets/settings.json").read())["num_of_players"]
                    num_of_decks = json.loads(open("assets/settings.json").read())["num_of_decks"]
                    game = BlackjackGame(number_of_players=num_of_players, number_of_decks=num_of_decks)
                    game.play()
                    screen = pygame.display.set_mode((800, 600))
                    screen.fill((0, 0, 0))
                    pygame.display.set_caption("Choose table")
                elif rect2.collidepoint(event.pos):
                    num_of_players = json.loads(open("assets/settings.json").read())["num_of_players"]
                    num_of_decks = json.loads(open("assets/settings.json").read())["num_of_decks"]
                    game = BlackjackGame(number_of_players=num_of_players, number_of_decks=num_of_decks, first_table=False)
                    game.play()
                    screen = pygame.display.set_mode((800, 600))
                    screen.fill((0, 0, 0))
                    pygame.display.set_caption("Choose table")

        pygame.draw.rect(screen, (34, 139, 34), rect1)
        draw_text('Table 1', (255, 255, 255), screen, 150, 50)
        draw_text('bots are playing with', (255, 255, 255), screen, 100, 400)
        draw_text('base strategy', (255,255,255), screen, 150, 430)
        pygame.draw.rect(screen, (0, 0, 255), rect2)
        draw_text('Table 2', (255, 255, 255), screen, 500, 50)
        draw_text('bots are counting cards', (255, 255, 255), screen, 450, 400)

        pygame.display.flip()
        clock.tick(60)