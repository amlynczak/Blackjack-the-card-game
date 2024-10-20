from blackjack.game import BlackjackGame

def main():
    num_decks = 0
    while(num_decks < 1 or num_decks > 8):
        num_decks = int(input("Put the number of decks you want to play with (1-8): "))

    num_players = 0
    while(num_players < 1 or num_players > 7):
        num_players = int(input("Put the number of players you want to play with (1-7): "))
    
    game = BlackjackGame(num_decks=num_decks, num_players=num_players)
    
    while True:
        game.play()
        play_again = input("Want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            break

if __name__ == "__main__":
    main()