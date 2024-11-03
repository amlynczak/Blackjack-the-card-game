from ui.starting_screen import StartScreen
from ui.game_screen import BlackjackGame
import json

def main():
    #num_of_players = json.loads(open("assets/settings.json").read())["num_of_players"]
    #num_of_decks = json.loads(open("assets/settings.json").read())["num_of_decks"]
    #game = BlackjackGame(number_of_players=num_of_players, number_of_decks=num_of_decks)
    #game.play()

    start_screen = StartScreen()
    start_screen.run()

if __name__ == "__main__":
    main()