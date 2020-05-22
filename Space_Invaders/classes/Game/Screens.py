import pygame
from pygame.locals import *
try:
    from .Enums import State, Direction
    from .Colors import *
    from .Player import Player
except ImportError:
    from Enums import State, Direction
    from Colors import *
    from Player import Player

#Initialise the fonts
pygame.font.init()

class Screen(object):
    font = pygame.font.Font(pygame.font.get_default_font(),15)
    end_font = pygame.font.Font(pygame.font.get_default_font(),30)
    title_font = pygame.font.Font(pygame.font.get_default_font(), 60)
    def __init__(self, game_width, game_height, state, screen):
        """Base Screen object
            Arguments:
                game_width: Width of the game in pixels
                game_height: Height of the game in pixels
                state: State that the game is in
                screen: Screen that the game will be blited to
        """

        #Store the variables
        self.screen = screen
        self.state = state
        self.game_width = game_width
        self.game_height = game_height

        #Create a surface with a transparent background
        self.surface = pygame.Surface((game_width,game_height), pygame.SRCALPHA, 32)

    def update(self) -> None:
        self.screen.blit(self.surface.convert_alpha(), (0,0))

    def reset(self) -> None:
        self.surface = pygame.Surface((self.game_width, self.game_height), pygame.SRCALPHA, 32)
    
    def handle(self) -> State:
        return self.state

    def write(self, font_type, color, words, xpos, ypos, direction = Direction.CENTER):
        sentence = font_type.render(words, True, color)

        if direction == Direction.CENTER:
            rect = sentence.get_rect(center = (xpos,ypos))
        elif direction == Direction.LEFT:
            rect = sentence.get_rect(left = xpos, top = ypos)
        elif direction == Direction.RIGHT:
            rect_sentence = sentence.get_rect(right = xpos, top = ypos)
        else:
            assert False, "Invalid write justification"

        self.surface.blit(sentence,rect)
        return rect

    def check_clicked(self, rect) -> bool:
        """Check if the player clicked on the rect"""

        #Get the position of the mouse
        mouse_pos = pygame.mouse.get_pos()

        #If player pressed the button
        return pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos)

def main() -> None:
    pass

if __name__ == '__main__':
    main()


