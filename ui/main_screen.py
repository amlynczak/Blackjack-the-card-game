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

def draw_button(text, font, color, surface, x, y, width, height):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, font, (0, 0, 0), surface, x + 10, y + 10)

def start_ui():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 55)
    button_font = pygame.font.SysFont(None, 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 300 <= mouse_x <= 500 and 200 <= mouse_y <= 250:
                    game_ui()
                elif 300 <= mouse_x <= 500 and 300 <= mouse_y <= 350:
                    show_rules()
                elif 300 <= mouse_x <= 500 and 400 <= mouse_y <= 450:
                    show_tutorial()

        # Fill the background
        screen.fill(BG_COLOR)

        # Draw buttons
        draw_button('Rozpocznij grę', button_font, (255, 255, 255), screen, 300, 200, 200, 50)
        draw_button('Zasady gry', button_font, (255, 255, 255), screen, 300, 300, 200, 50)
        draw_button('Samouczek', button_font, (255, 255, 255), screen, 300, 400, 200, 50)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

def game_ui():
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

def show_rules():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                start_ui()

        # Fill the background
        screen.fill(BG_COLOR)

        # Draw rules text
        draw_text('Zasady gry:', font, (255, 255, 255), screen, 50, 50)
        draw_text('1. Celem gry jest uzyskanie sumy punktów jak najbliższej 21.', font, (255, 255, 255), screen, 50, 100)
        draw_text('2. Gracz i krupier otrzymują po dwie karty.', font, (255, 255, 255), screen, 50, 150)
        draw_text('3. Gracz może dobierać karty, aż zdecyduje się zatrzymać.', font, (255, 255, 255), screen, 50, 200)
        draw_text('4. Krupier dobiera karty, aż osiągnie co najmniej 17 punktów.', font, (255, 255, 255), screen, 50, 250)
        draw_text('5. Jeśli suma punktów gracza przekroczy 21, przegrywa.', font, (255, 255, 255), screen, 50, 300)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

def show_tutorial():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                start_ui()

        # Fill the background
        screen.fill(BG_COLOR)

        # Draw tutorial text
        draw_text('Samouczek:', font, (255, 255, 255), screen, 50, 50)
        draw_text('1. Kliknij "Rozpocznij grę", aby rozpocząć nową grę.', font, (255, 255, 255), screen, 50, 100)
        draw_text('2. Kliknij "Zasady gry", aby zobaczyć zasady.', font, (255, 255, 255), screen, 50, 150)
        draw_text('3. Kliknij "Samouczek", aby zobaczyć ten samouczek.', font, (255, 255, 255), screen, 50, 200)
        draw_text('4. W grze, kliknij karty, aby je dobrać.', font, (255, 255, 255), screen, 50, 250)
        draw_text('5. Kliknij ESC, aby wrócić do ekranu startowego.', font, (255, 255, 255), screen, 50, 300)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    start_ui()