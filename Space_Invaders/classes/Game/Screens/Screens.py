import pygame
from pygame.locals import *
from .. import BaseObject, State, Direction

pygame.font.init()

class Screen(BaseObject):
    #Store the fonts in the Screen Object
    font = pygame.font.Font(pygame.font.get_default_font(),15)
    end_font = pygame.font.Font(pygame.font.get_default_font(),30)
    subtitle_font = pygame.font.Font(pygame.font.get_default_font(), 40)
    title_font = pygame.font.Font(pygame.font.get_default_font(), 60)

    def __init__(self, screen_width:int, screen_height:int, state:State, screen, initial_x:int, initial_y:int, debug:bool = False):
        """Base Screen object
            Arguments:
                screen_width: Width of the game in pixels (int)
                screen_height: Height of the game in pixels (int)
                state: State that the game is in (State)
                screen: Surface that the game will be blited to (pygame.Surface)
                debug: toggles debug mode (bool): default = False

            Methods:
                update: Blit the Screen onto the surface
                reset: Reset the Screen
                handle: Placeholder method to be overwritten
                write: Write Words onto the screen
                check_clicked: Checks of the rect is clicked on by user
        """
        #Call superclass
        super().__init__(initial_x, initial_y, debug)

        #Store the variables
        self.screen = screen
        self.state = state
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.debug = debug
        self.bg = None
        self.cooldown = 20

        #Create a surface with a transparent background
        self.reset_surface()

    def post_process(self):
        """Post processes after the screen updates 
           Does nothing
           Any process after updating the screen should be done here
        """
        pass

    def set_background(self, bg) -> None:
        """Update the background"""
        self.bg = bg
        self.surface.fill(self.bg)

    def reset_surface(self) -> None:
        """Reset the surface to a blank surface"""
        self.surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA, 32)

    def update(self) -> None:
        """Blits the screen onto the surface
            Arguments:
                No arguments
            Returns: 
                No returns
        """
        
        #If the screen has a background
        if self.bg:

            #Blit the screen without make it transparent
            self.screen.blit(self.surface, self.get_coord())

        #Otherwise
        else:

            #Blit the screen while making background transparent
            self.screen.blit(self.surface.convert_alpha(), self.get_coord())

    def set_state(self, state:State):
        """Set the current state of the screen"""
        self.state = state
    
    def handle(self) -> State:
        """Placeholder method to be overwritten
            Arguments:
                No arguments
            Returns: 
                Returns the next state the game is suppose to be in
        """
        return self.state

    def write_main(self,font_type, color: Color, words:str, xpos:int, ypos:int, direction:Direction = Direction.CENTER):
        """Write to main surface directly"""
        return self.write(font_type, color, words, xpos, ypos, direction, self.screen)

    def write(self, font_type, color: Color, words:str, xpos:int, ypos:int, direction:Direction = Direction.CENTER, screen = None) -> pygame.Rect:
        """Write words onto the screen
            Arguments:
                font_type: The type of font to be used (pygame.font)
                color: Color of the words (Color)
                words: Words to be printed (string)
                xpos: X coordinate of direction defined(int)
                ypos: Y coordinate of direction defined(int)

            Return:
                Rect containing the words created (pygame.Rect)
        """
        #If no screen is specified
        if screen == None:

            #Make it the surface
            screen = self.surface

        #Render the sentence using the font
        sentence = font_type.render(words, True, color)

        #If it is center justified
        if direction == Direction.CENTER:

            #Set the center position as xpos and ypos
            rect = sentence.get_rect(center = (xpos,ypos))

        #If it is left justified
        elif direction == Direction.LEFT:

            #Set the top left corner to the coordinate
            rect = sentence.get_rect(left = xpos, top = ypos)
        
        #If it is right justified
        elif direction == Direction.RIGHT:

            #Set the top right corner to the coordinate
            rect = sentence.get_rect(right = xpos, top = ypos)

        #Otherwise it is an invalid justification
        else:

            #Assert an Error
            assert False, f"Invalid write justification {direction}"

        #Draw the words onto the screen
        screen.blit(sentence,rect)

        #Return the rectangle object
        return rect

    def check_clicked(self, rect) -> bool:
        """Check if the player clicked on the rect
            Arguments:
                rect: The rectangle to be checked if the player clicked on it (pygame.Rect)
            Return: 
                returns a boolean indicating if the player clicked on the rect (bool)
        """

        #Get the position of the mouse
        mouse_pos = pygame.mouse.get_pos()

        #Return if the mouse position is within the rect and the player clicked
        return pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos)


