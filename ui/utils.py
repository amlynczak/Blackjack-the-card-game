import pygame
import sys
import math

pygame.init()

GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 255)
CARD_WIDTH, CARD_HEIGHT = 60, 90

font = pygame.font.Font(None, 36)

card_images = {}
card_images_bots = {}
card_images['back'] = pygame.transform.scale(pygame.image.load("assets/images/cards/back.jpg"), (CARD_WIDTH, CARD_HEIGHT))
card_images_bots['back'] = pygame.transform.scale(pygame.image.load("assets/images/cards/back.jpg"), (CARD_WIDTH * 0.66, CARD_HEIGHT * 0.66))
for suit in ['spades', 'hearts', 'diamonds', 'clubs']:
    for value in range(2, 11):
        card_images[f"{value}_of_{suit}"] = pygame.transform.scale(pygame.image.load(f"assets/images/cards/{value}_of_{suit}.png"), (CARD_WIDTH, CARD_HEIGHT))
        card_images_bots[f"{value}_of_{suit}"] = pygame.transform.scale(pygame.image.load(f"assets/images/cards/{value}_of_{suit}.png"), (CARD_WIDTH * 0.66, CARD_HEIGHT * 0.66))
    for face in ['J', 'Q', 'K', 'A']:
        card_images[f"{face}_of_{suit}"] = pygame.transform.scale(pygame.image.load(f"assets/images/cards/{face}_of_{suit}.png"), (CARD_WIDTH, CARD_HEIGHT))
        card_images_bots[f"{face}_of_{suit}"] = pygame.transform.scale(pygame.image.load(f"assets/images/cards/{face}_of_{suit}.png"), (CARD_WIDTH * 0.66, CARD_HEIGHT * 0.66))


def draw_text(text, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_text_rotated(text, color, surface, x, y, angle):
    text_surface = font.render(text, True, color)
    rotated_text = pygame.transform.rotate(text_surface, angle)
    rect = rotated_text.get_rect()
    surface.blit(rotated_text, (x - rect.width//2, y - rect.height//2))

def draw_button(text, color, surface, x, y, width, height):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, (0, 0, 0), surface, x + 10, y + 10)

def draw_button_unavailable(text, color, surface, x, y, width, height):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, (0, 0, 0), surface, x + 10, y + 10)

def draw_background(screen, counting_prohibited=True):
    if counting_prohibited:
        screen.fill(GREEN)
    else:
        screen.fill(DARK_BLUE)
    #circle_center = (screen.get_width()//2, 0)
    #radius = 200
    #texts = ["BLACKJACK PAY 3 TO 2", "DEALER MUST HIT ON SOFT 17", "INSURANCE PAYS 2 TO 1"]
    #pygame.draw.circle(screen, WHITE, circle_center, radius, 5)
    #start_angle = 180
    #angle_step = 360 // len(texts)
    #for i, text in enumerate(texts):
    #    angle = start_angle + i * angle_step
    #    x = circle_center[0] + int(radius * math.cos(math.radians(angle)))
    #    y = circle_center[1] + int(radius * math.sin(math.radians(angle)))
    #    text_angle = -angle
    #    draw_text_rotated(text, pygame.font.Font(None, 36), WHITE, screen, x, y, angle)
    pygame.display.flip()


def display_game_state(screen, main_player, dealer, bot_players, counting_prohibited = True, dealer_show_all=False, players_turn=False):
        draw_background(screen, counting_prohibited)
        
        players_step = screen.get_width() // (len(main_player.hands) + 1)
        for i, hand in enumerate(main_player.hands):
            shift = 30 + 15 * (hand.cards.__len__() - 1)
            x = (i + 1) * players_step
            y = screen.get_height() - 200
            display_hand(hand, x - shift, y, screen)
        shift = 30 + 50 * (dealer.hand.__len__() - 1)
        display_hand_dealer(dealer, screen.get_width()//2 - shift , 20, screen, dealer_show_all)

        center_y = 80
        radius = 300

        bots_right_side = bot_players[:len(bot_players)//2]
        right_side_hands = []
        for bot in bots_right_side:
            right_side_hands.extend(bot.hands)
        if len(right_side_hands) != 0:
            angle_step_right = 90 // len(right_side_hands)
            center_x_right_side = screen.get_width() // 2 + 260
            for i, hand in enumerate(right_side_hands):
                angle = (i + 1) * angle_step_right
                x = center_x_right_side + int(radius * math.cos(math.radians(angle)))
                y = center_y + int(radius * math.sin(math.radians(angle)))
                display_hand_bot(hand, x, y, screen, True)

        bots_left_side = bot_players[len(bot_players)//2:]
        left_side_hands = []
        for bot in bots_left_side:
            left_side_hands.extend(bot.hands)
        if len(left_side_hands) != 0:
            angle_step_left = 90 // len(left_side_hands)
            center_x_left_side = screen.get_width() // 2 - 300
            for i, hand in enumerate(left_side_hands):
                angle = i * angle_step_left + 90
                x = center_x_left_side + int(radius * math.cos(math.radians(angle)))
                y = center_y + int(radius * math.sin(math.radians(angle)))
                display_hand_bot(hand, x, y, screen, False)
        
        if players_turn:
            if main_player.can_hit(main_player.hand_id):
                draw_button("Hit", WHITE, screen, 20, screen.get_height()-120, 100, 50)
            if main_player.can_stand():
                draw_button("Stand", WHITE, screen, 20, screen.get_height()-60, 100, 50)
            if main_player.can_double_down(main_player.hand_id):
                draw_button("Double", WHITE, screen, 130, screen.get_height()-120, 100, 50)
            if main_player.can_split():
                draw_button("Split", WHITE, screen, 130, screen.get_height()-60, 100, 50)
            if main_player.can_insurance(dealer.hand):
                draw_button("Insurance", WHITE, screen, 240, screen.get_height()-120, 100, 50)
            if main_player.can_surrender():
                draw_button("Surrender", WHITE, screen, 240, screen.get_height()-60, 100, 50)
        pygame.display.flip()

def display_hand(hand, x, y, screen):
    for j, card in enumerate(hand.cards):
        if hand.has_doubled_down and j == 2:
            card_img = pygame.transform.rotate(card_images[str(card)], 90)
        else:
            card_img = card_images[str(card)]
        screen.blit(card_img, (x + j * 30, y - j * 10))
    text = font.render(f"{hand.name}: {hand.get_hand_value()}", True, WHITE)
    screen.blit(text, (x, y + 100))
    if hand.isBlackjack:
        text = font.render("Blackjack!", True, WHITE)
        screen.blit(text, (x + 200, y + 100))

def display_hand_bot(hand, x, y, screen, right_hand_side=True):
    font = pygame.font.Font(None, 18)
    for j, card in enumerate(hand.cards):
        card_img = card_images_bots[str(card)]
        if hand.has_doubled_down and j == 2:
            card_img = pygame.transform.rotate(card_img, 90)
        
        if right_hand_side:
            screen.blit(card_img, (x - j * 20, y - j * 20))
        else:
            screen.blit(card_img, (x + j * 20, y - j * 20))
    text = font.render(f"{hand.name}({hand.get_hand_value()})", True, WHITE)
    screen.blit(text, (x - 20, y + 65))

def display_hand_dealer(dealer, x, y, screen, show_all=False):
    for i, card in enumerate(dealer.hand):
        if i == 0:
            screen.blit(card_images[str(card)], (x + i * 100, y))
        elif show_all:
            screen.blit(card_images[str(card)], (x + i * 100, y))
        else:
            screen.blit(card_images['back'], (x + i * 100, y))
    
    if not show_all:
        text = font.render(f"Dealer: {dealer.hand[0]} and [hidden]", True, WHITE)
    else:
        text = font.render(f"Dealer: {dealer.get_hand_value()}", True, WHITE)
    screen.blit(text, (x, y + 100))