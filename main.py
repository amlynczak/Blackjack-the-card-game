from blackjack.game import BlackjackGame

def main():
    num_decks = 0
    while(num_decks < 1 or num_decks > 8):
        num_decks = int(input("Podaj liczbę talii kart(1-8): "))

    num_players = 0
    while(num_players < 1 or num_players > 7):
        num_players = int(input("Podaj liczbę graczy - wliczając Ciebie(1-7): "))
    
    game = BlackjackGame(num_decks=num_decks, num_players=num_players)
    
    while True:
        game.play()
        play_again = input("Czy chcesz zagrać jeszcze raz? (tak/nie): ").lower()
        if play_again != 'tak':
            break

if __name__ == "__main__":
    main()