import pygame
import os
import sys

from ui.utils import draw_button, draw_text
from ui.settings import settings
from ui.rules import show_rules
from ui.tables import choose_table

os.environ['SDL_VIDEO_CENTERED'] = '1'

class StartScreen:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer module
        pygame.mixer.music.load('assets/music/FLOWERS.mp3')  # Load the music file
        pygame.mixer.music.play(-1)  # Play the music in a loop
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("♣♦♥♠ Blackjack game ♣♦♥♠")
        self.clock = pygame.time.Clock()
        self.screen.fill((0, 0, 0))

    def run(self):
        self.screen.fill((0, 0, 0))
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if 300 <= mouse_x <= 500 and 200 <= mouse_y <= 250:
                        choose_table(self.screen)
                    elif 300 <= mouse_x <= 500 and 300 <= mouse_y <= 350:
                        show_rules(self.screen)
                    elif 300 <= mouse_x <= 500 and 400 <= mouse_y <= 450:
                        settings(self.screen)

            self.screen.fill((0, 0, 0))

            draw_text('Blackjack playing app', (255, 255, 255), self.screen, 225, 50)

            draw_button('Rozpocznij grę', (255, 255, 255), self.screen, 300, 200, 200, 50)
            draw_button('Zasady gry', (255, 255, 255), self.screen, 300, 300, 200, 50)
            draw_button('Ustawienia', (255, 255, 255), self.screen, 300, 400, 200, 50)

            pygame.display.flip()
            self.clock.tick(30)