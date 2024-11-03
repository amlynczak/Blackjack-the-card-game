import pygame
import sys
import json

from ui.utils import draw_button, draw_text
from ui.game_screen import BlackjackGame

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
                    game = BlackjackGame(screen, number_of_players=num_of_players, number_of_decks=num_of_decks)
                    game.play()
                    screen = pygame.display.set_mode((800, 600), )
                    screen.fill((0, 0, 0))
                    pygame.display.set_caption("Choose table")
                elif rect2.collidepoint(event.pos):
                    return 'table2'

        pygame.draw.rect(screen, (34, 139, 34), rect1)
        draw_text('Table 1', button_font, (255, 255, 255), screen, 150, 200)
        draw_text('base bet: 20', button_font, (255, 255, 255), screen, 150, 250)
        draw_text('can surrender', button_font, (255, 255, 255), screen, 150, 300)
        draw_text('can double', button_font, (255, 255, 255), screen, 150, 350)
        draw_text('can split', button_font, (255, 255, 255), screen, 150, 400)
        draw_text('can insure', button_font, (255, 255, 255), screen, 150, 450)
        pygame.draw.rect(screen, (0, 0, 255), rect2)
        draw_text('Table 2', button_font, (255, 255, 255), screen, 500, 200)
        draw_text('base bet: 50', button_font, (255, 255, 255), screen, 500, 250)
        draw_text('cannot surrender', button_font, (255, 255, 255), screen, 500, 300)
        draw_text('can double', button_font, (255, 255, 255), screen, 500, 350)
        draw_text('can split', button_font, (255, 255, 255), screen, 500, 400)
        draw_text('can insure', button_font, (255, 255, 255), screen, 500, 450)

        pygame.display.flip()
        clock.tick(60)