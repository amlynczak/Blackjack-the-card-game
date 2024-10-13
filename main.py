from blackjack.game import BlackjackGame

def main():
    num_decks = int(input("Podaj liczbę talii kart: "))
    num_players = int(input("Podaj liczbę graczy (w tym siebie): "))
    
    game = BlackjackGame(num_decks=num_decks, num_players=num_players)
    
    while True:
        game.play()
        play_again = input("Czy chcesz zagrać jeszcze raz? (tak/nie): ").lower()
        if play_again != 'tak':
            break

if __name__ == "__main__":
    main()