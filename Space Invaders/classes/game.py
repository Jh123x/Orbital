import pygame


class GameWindow():
    """The main game window for Space invaders"""
    def __init__(self, sensitivity:int, maxfps:int, game_width:int, game_height:int):
        """The constructor for the main window"""
        self.sensitivity = sensitivity
        self.maxfps = maxfps
        self.game_width = game_width
        self.game_height = game_height

    def mainloop(self) -> None:
        """The mainloop to run the game"""
        pass

def main() -> None:
    """The main function for the file"""
    pass

#Run the main function if this file is main
if __name__ == "__main__":
    main()