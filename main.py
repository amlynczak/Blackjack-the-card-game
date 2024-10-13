from blackjack.game import BlackjackGame

def main():
    game = BlackjackGame(num_decks=1)
    
    while True:
        game.play()
        play_again = input("Czy chcesz zagrać jeszcze raz? (tak/nie): ").lower()
        if play_again != 'tak':
            break

if __name__ == "__main__":
    main()