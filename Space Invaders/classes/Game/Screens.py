import pygame
from .Enums import State

class Screen(pygame.Surface):
    def __init__(self, game_width:int, game_height:int, state: State):
        """The main Screen class"""

        #Call the super class
        super().__init__((game_width,game_height))

        #Define the state
        self.state = State

    
    def draw(self) -> None:
        pass

    def check_clicked(self, *rect) -> None:
        pass
    


def main() -> None:
    pass

if __name__ == '__main__':
    main()