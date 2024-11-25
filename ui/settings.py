import pygame
import sys

from ui.utils import draw_button, draw_text

def settings(screen):
    screen.fill((0, 0, 0))
    pygame.display.set_caption("Settings")

    button_font = pygame.font.SysFont(None, 35)
    clock = pygame.time.Clock()

    input_boxes = [pygame.Rect(300, 200, 200, 50), pygame.Rect(300, 300, 200, 50)]
    input_texts = ['Number of decks', 'Number of players', 'Language', 'counting method used']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 300 <= mouse_x <= 500 and 500 <= mouse_y <= 550:
                    return input_boxes

        screen.fill((0, 0, 0))
        draw_button('Save', button_font, (255, 255, 255), screen, 300, 500, 200, 50)

        for i, box in enumerate(input_boxes):
            pygame.draw.rect(screen, (255, 255, 255), box)
            draw_text(input_texts[i], button_font, (0, 0, 0), screen, box.x + 10, box.y + 10)

        pygame.display.flip()
        clock.tick(30)

    screen.fill((0, 0, 0))

        