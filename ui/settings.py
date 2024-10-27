import pygame
import sys

from ui.utils import draw_button, draw_text

def settings():
    settings_screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Ustawienia")

    font = pygame.font.SysFont(None, 35)
    
    input_boxes = {
        "bg_color": pygame.Rect(300, 20, 250, 30),
        "font_size": pygame.Rect(300, 60, 250, 30),
        "font": pygame.Rect(300, 100, 250, 30),
        "num_players": pygame.Rect(300, 180, 250, 30),
        "num_decks": pygame.Rect(300, 220, 250, 30),
        "bet_size": pygame.Rect(300, 260, 250, 30)
    }
    input_texts = {
        "bg_color": "",
        "font_size": "",
        "font": "",
        "num_players": "",
        "num_decks": "",
        "bet_size": ""
    }
    active_box = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for box in input_boxes:
                    if input_boxes[box].collidepoint(event.pos):
                        active_box = box
                    else:
                        active_box = None
            if event.type == pygame.KEYDOWN:
                if active_box:
                    if event.key == pygame.K_BACKSPACE:
                        input_texts[active_box] = input_texts[active_box][:-1]
                    else:
                        input_texts[active_box] += event.unicode

        # Fill the background
        settings_screen.fill((34, 139, 34))

        draw_text('Background Color:', font, (255, 255, 255), settings_screen, 10, 20)
        draw_text('Font Size:', font, (255, 255, 255), settings_screen, 10, 60)
        draw_text('Font:', font, (255, 255, 255), settings_screen, 10, 100)
        draw_text('Number of Players:', font, (255, 255, 255), settings_screen, 10, 180)
        draw_text('Number of Decks:', font, (255, 255, 255), settings_screen, 10, 220)
        draw_text('Standard Bet Size:', font, (255, 255, 255), settings_screen, 10, 260)

        for key, box in input_boxes.items():
            pygame.draw.rect(settings_screen, (255, 255, 255), box, 2)
            draw_text(input_texts[key], font, (255, 255, 255), settings_screen, box.x + 5, box.y + 5)

        draw_button('Save', font, (255, 255, 255), settings_screen, 250, 320, 100, 30)

        pygame.display.flip()

        