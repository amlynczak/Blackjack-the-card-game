from blackjack import Card, Deck, BlackjackGame
#import card_counter
#import ui

def main():
    game = BlackjackGame(num_decks=1)  # Gra z jedną talią
    game.play()  # Rozpocznij rozgrywkę

if __name__ == "__main__":
    main()
