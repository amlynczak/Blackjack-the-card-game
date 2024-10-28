import pygame
import sys

from blackjack.game import BlackjackGame
from ui.utils import draw_button, draw_text, draw_card
from blackjack.card import Card

class GameScreen:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), )
        pygame.display.set_caption("♣♦♥♠ Blackjack game ♣♦♥♠")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 55)
        self.button_font = pygame.font.SysFont(None, 35)
        self.screen.fill((0, 0, 0))
        self.game = BlackjackGame()

    def run(self):
        self.screen.fill((0, 0, 0))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
            draw_card(self.screen, None, 100, 100)

            #self.game.play()