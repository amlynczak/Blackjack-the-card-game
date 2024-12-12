import pygame
import sys
import json

from ui.utils import draw_button, draw_text

def save_settings(settings):
    with open('assets/settings.json', 'w') as f:
        json.dump(settings, f)

def settings(screen):
    screen.fill((0, 0, 0))
    pygame.display.set_caption("Settings")

    button_font = pygame.font.SysFont(None, 35)
    clock = pygame.time.Clock()

    settings = {
        'number_of_decks': 1,
        'number_of_players': 1,
        'counting_method': 'halves'
    }

    options = {
        'number_of_decks': [1, 2, 4, 6, 8],
        'number_of_players': [1, 2, 3, 4, 5, 6, 7],
        'counting_method': ['halves', 'high_low', 'high_optI', 'high_optII', 'ko', 'omega', 'red_seven', 'ten_count', 'zen_count']
    }

    input_boxes = [pygame.Rect(200, 100, 400, 50), pygame.Rect(200, 200, 400, 50), pygame.Rect(200, 300, 400, 50)]
    input_texts = ['Liczba talii kart', 'Liczba graczy przy stole', 'Metoda liczenia kart']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 300 <= mouse_x <= 500 and 500 <= mouse_y <= 550:
                    save_settings(settings)
                    return input_boxes
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(mouse_x, mouse_y):
                        key = list(settings.keys())[i]
                        current_index = options[key].index(settings[key])
                        settings[key] = options[key][(current_index + 1) % len(options[key])]

        screen.fill((0, 0, 0))
        draw_button('Zapisz', (255, 255, 255), screen, 300, 500, 200, 50)

        for i, box in enumerate(input_boxes):
            pygame.draw.rect(screen, (255, 255, 255), box)
            key = list(settings.keys())[i]
            draw_text(f"{input_texts[i]}: {settings[key]}", (0, 0, 0), screen, box.x + 10, box.y + 10)

        pygame.display.flip()
        clock.tick(30)

