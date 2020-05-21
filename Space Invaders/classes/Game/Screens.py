import pygame
from pygame.locals import *
try:
    from .Enums import State, Direction
    from .Colors import *
except ImportError:
    from Enums import State, Direction
    from Colors import *

#Initialise the fonts
pygame.font.init()

class Screen(object):
    def __init__(self, game_width, game_height, state, screen):
        self.screen = screen
        self.surface = pygame.Surface((game_width,game_height), pygame.SRCALPHA, 32)
        self.state = state
        self.game_width = game_width
        self.game_height = game_height
        self.font = pygame.font.Font(pygame.font.get_default_font(),game_width//40)
        self.end_font = pygame.font.Font(pygame.font.get_default_font(),game_width//20)
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), game_width // 10)

    def update(self) -> None:
        self.screen.blit(self.surface.convert_alpha(), (0,0))
    
    def handle(self) -> State:
        return self.state

    def write(self, font_type, color, words, xpos, ypos, direction = Direction.CENTER):
        sentence = font_type.render(words, True, color)

        if direction == Direction.CENTER:
            rect = sentence.get_rect(center = (xpos,ypos))

        elif direction == Direction.LEFT:
            rect = sentence.get_rect(left = xpos, top = ypos)

        self.surface.blit(sentence,rect)
        return rect

    def check_clicked(self, rect) -> bool:
        """Check if the player clicked on the rect"""

        #Get the position of the mouse
        mouse_pos = pygame.mouse.get_pos()

        #If player pressed the button
        return pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos)

class InstructionScreen(Screen):
    def __init__(self, game_width, game_height, screen):
        super().__init__(game_width, game_height, State.INSTRUCTIONS, screen)

        #The first pixel to align
        first_px = self.game_height//2

        #Draw the header
        self.write(self.title_font, WHITE, "Instructions", self.game_width//2, first_px - self.game_height//5)

        #Draw the instructions
        self.write(self.end_font, WHITE, "Use AD or arrow keys to move", self.game_width//2, first_px)
        self.write(self.end_font, WHITE, "Press spacebar to shoot, P to pause", self.game_width//2, first_px + self.game_height//15)
        self.write(self.end_font, WHITE, "Press O to unpause", self.game_width//2, first_px + self.game_height//7.5)

        #Draw the back button
        self.back_rect = self.write(self.end_font,WHITE, "Back", self.game_width//2, self.game_height-self.game_height//5)

    def handle(self) -> State:
        """Load the Instructions onto the screen
            Arguments:
                No Arguments
            Returns:
                Returns the State the game should be in
        """

        #Update onto the screen
        self.update()

        #Check if the back button is clicked
        if self.check_clicked(self.back_rect):
            return State.MENU

        #Otherwise return the current state
        return self.state

class MenuScreen(Screen):
    def __init__(self, game_width, game_height, screen):

        #Call the superclass
        super().__init__(game_width, game_height, State.MENU, screen)

        #Draw the title
        self.write(self.title_font, WHITE, "Space Invaders", self.game_width//2, self.game_height//5)

        #Draw the Play button
        self.rect_play = self.write(self.end_font,WHITE, "Play", self.game_width//2, self.game_height//2)

        #Draw the highscore button
        self.rect_highscore = self.write(self.end_font, WHITE, "High Score", self.game_width//2, self.game_height//15 + self.game_height//2)

        #Draw the instructions button
        self.rect_instruction = self.write(self.end_font, WHITE, "Instructions", self.game_width//2, self.game_height//7.5 + self.game_height//2)

        #Draw the quit button
        self.rect_end = self.write(self.end_font, WHITE, "Quit", self.game_width//2, self.game_height//5 + self.game_height//2)


    def update_keypresses(self) -> State:
        """Track the keypress for the menu"""
        #Get the keypresses of the user
        keys = pygame.key.get_pressed()

        #Check if the user press the return key
        if keys[K_RETURN]:

            #Start the game
            return State.PLAY

        #Check if the user epressed the escape key
        elif keys[K_ESCAPE]:

            #Quit the game
            return State.QUIT

        else:

            #Otherwise return none
            return None


    def check_mouse_pos(self, rect_play, rect_end, rect_highscore, rect_instructions):
        """Check the position of the mouse on the menu to see what the player clicked"""

        #If mousedown and position colide with play
        if self.check_clicked(rect_play):
            return State.PLAY

        #If mousedown and position colide with quit
        elif self.check_clicked(rect_end):
            return State.QUIT

        elif self.check_clicked(rect_highscore):
            return State.HIGHSCORE
        
        elif self.check_clicked(rect_instructions):
            return State.INSTRUCTIONS

        #Otherwise the player has not decided
        else:
            #Return menu state
            return State.MENU

    def handle(self) -> State:
        """Load the Menu onto the screen
            Arguments:
                No Arguments
            Returns:
                Returns the State the game should be in
        """
        self.update()

        #Get the keypresses of the player
        state = self.update_keypresses()

        #Check the position of the mouse to return the state
        return state if state else self.check_mouse_pos(self.rect_play, self.rect_end, self.rect_highscore, self.rect_instruction)

def main() -> None:
    game_height = 800
    game_width = 600
    screen = pygame.display.set_mode((game_width,game_height))
    clock = pygame.time.Clock()
    fps = 60

    inst = InstructionScreen(game_width,game_height,screen)

    while True:
        #Set the FPS
            clock.tick(fps)

            inst.handle()

            #Update the display with the screen
            pygame.display.update()

            #If the state is quit or player closes the game
            if pygame.QUIT in tuple(map(lambda x: x.type, pygame.event.get())):
                break

if __name__ == '__main__':
    main()


