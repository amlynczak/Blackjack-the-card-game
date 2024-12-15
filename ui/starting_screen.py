import pygame
import os
import sys

from ui.utils import draw_button, draw_text, draw_title
from ui.settings import settings
from ui.rules import show_rules
from ui.tables import choose_table

os.environ['SDL_VIDEO_CENTERED'] = '1'

class StartScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("♣♦♥♠ Blackjack app ♣♦♥♠")
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
                        pygame.display.set_caption("♣♦♥♠ Blackjack app ♣♦♥♠")
                    elif 300 <= mouse_x <= 500 and 300 <= mouse_y <= 350:
                        show_rules(self.screen)
                        pygame.display.set_caption("♣♦♥♠ Blackjack app ♣♦♥♠")
                    elif 300 <= mouse_x <= 500 and 400 <= mouse_y <= 450:
                        settings(self.screen)
                        pygame.display.set_caption("♣♦♥♠ Blackjack app ♣♦♥♠")

            self.screen.fill((0, 0, 0))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/images/suits/spades.png"), (100, 200)), (75, 100))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/images/suits/hearts.png"), (100, 200)), (75, 350))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/images/suits/diamonds.png"), (100, 200)), (625, 100))
            self.screen.blit(pygame.transform.scale(pygame.image.load("assets/images/suits/clubs.png"), (100, 200)), (625, 350))

            draw_title('Blackjack - gra karciana', (255, 255, 255), self.screen, 50)

            draw_button('Rozpocznij grę', (255, 255, 255), self.screen, 300, 200, 200, 50)
            draw_button('Zasady gry', (255, 255, 255), self.screen, 300, 300, 200, 50)
            draw_button('Ustawienia', (255, 255, 255), self.screen, 300, 400, 200, 50)

            pygame.display.flip()
            self.clock.tick(30)