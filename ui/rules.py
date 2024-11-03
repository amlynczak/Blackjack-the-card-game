import pygame
import sys

from ui.utils import draw_button, draw_text

def show_rules(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 300 <= mouse_x <= 500 and 500 <= mouse_y <= 550:
                    return

        screen.fill((0, 0, 0))


        draw_text('Zasady gry', font, (255, 255, 255), screen, 300, 50)
        draw_text('1. Gracz (lub gracze) i krupier otrzymują po dwie karty.', font, (255, 255, 255), screen, 50, 100)
        draw_text('2. Celem gry jest uzyskanie sumy punktów jak najbliższej 21.', font, (255, 255, 255), screen, 50, 150)
        draw_text('3. Gracz ma możliwość dobierania kolejnych kart.', font, (255, 255, 255), screen, 50, 200)
        draw_text('4. Gracz przegrywa, jeśli przekroczy 21 punktów.', font, (255, 255, 255), screen, 50, 250)
        draw_text('5. Krupier dobiera karty, aż osiągnie co najmniej 17 punktów.', font, (255, 255, 255), screen, 50, 300)
        draw_text('6. Gracz wygrywa, jeśli ma więcej punktów niż krupier.', font, (255, 255, 255), screen, 50, 350)

        draw_button('Back', pygame.font.SysFont(None, 35), (255, 255, 255), screen, 300, 500, 200, 50)

        pygame.display.flip()
        clock.tick(30)