import pygame
import sys
import os

from ui.utils import draw_button, draw_text

os.environ['SDL_VIDEO_CENTERED'] = '1'

def show_rules(screen): 
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1300, 600))
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

        draw_text('Zasady gry', (255, 255, 255), screen, 590, 50)

        # Left column
        draw_text('1. Gracze przy stole (oraz krupier) otrzymują po dwie karty.', (255, 255, 255), screen, 20, 100)
        draw_text('2. Celem jest uzyskanie sumy punktów najbliższej 21.', (255, 255, 255), screen, 20, 150)
        draw_text('3. Karty od 2 do 10 mają tyle punktów, ile mają wypisane,', (255, 255, 255), screen, 20, 200)
        draw_text('   J, Q, K mają 10 punktów, As ma 1 lub 11 punktów.', (255, 255, 255), screen, 20, 230)
        draw_text('4. Gracz może wykonać akcje:', (255, 255, 255), screen, 20, 280)
        draw_text('   - "HIT" - dobranie karty,', (255, 255, 255), screen, 30, 310)
        draw_text('   - "STAND" - zakończenie tury,', (255, 255, 255), screen, 30, 340)
        draw_text('   - "DOUBLE DOWN" - dobranie karty i podwojenie stawki,', (255, 255, 255), screen, 30, 370)
        draw_text('     (tylko, gdy gracz ma dwie karty na ręce),', (255, 255, 255), screen, 30, 400)
        draw_text('   - "SPLIT" - rozdzielenie kart na dwie ręce,', (255, 255, 255), screen, 30, 430)
        draw_text('     (tylko jeśli ranga kart jest taka sama),', (255, 255, 255), screen, 30, 460)

        # Right column
        draw_text('   - "INSURANCE" - ubezpieczenie w razie Blackjacka,', (255, 255, 255), screen, 700, 100)
        draw_text('     (tylko, jeśli odkryta karta krupiera to As),', (255, 255, 255), screen, 700, 130)
        draw_text('   - "SURRENDER" - poddanie się, zwrot zakładu 1:2,', (255, 255, 255), screen, 700, 160)
        draw_text('     (tylko jako pierwsza akcja).', (255, 255, 255), screen, 700, 190)
        draw_text('5. Gracz przegrywa, jeśli przekroczy 21 punktów.', (255, 255, 255), screen, 700, 240)
        draw_text('6. Dealer dobiera karty do 17 punktów.', (255, 255, 255), screen, 700, 270)
        draw_text('7. Dealer przegrywa, jeśli przekroczy 21 punktów.', (255, 255, 255), screen, 700, 300)
        draw_text('8. Wygrywa ten, kto ma więcej punktów niż przeciwnik.', (255, 255, 255), screen, 700, 330)
        draw_text('   (ale nie więcej niż 21).', (255, 255, 255), screen, 700, 360)
        draw_text('9. W przypadku gdy gracz ma Blackajcka (As i K/Q/J/10),', (255, 255, 255), screen, 700, 390)
        draw_text('   wygrywa w stosunku 3:2 do postawionej stawki.', (255, 255, 255), screen, 700, 420)

        draw_button('Back', (255, 255, 255), screen, 550, 500, 200, 50)

        pygame.display.flip()
        clock.tick(30)