import pygame
from pygame.locals import *
from . import Screen
from .. import State, WHITE, ImageObject

class MenuScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """Constructor for the Main Menu screen"""

        #Call the superclass
        super().__init__(screen_width, screen_height, State.MENU, screen, 0, 0, debug)

        #Write content for menu screen
        self.write_lines()

        #Store the rects and the effects
        self.rects = (self.rect_play, self.rect_highscore, self.rect_instruction, self.rect_settings, self.rect_end)
        self.effects = (State.PLAYMODE, State.HIGHSCORE, State.INSTRUCTIONS_MENU, State.SETTINGS, State.QUIT)

        #Reset the menu
        self.reset()

    def reset(self) -> None:
        """Reset the menu to default state"""
        #Show the menu currently selected
        self.selected = 0

        #Refresh pointer cd
        self.pointer_cd = 20
        
    def refresh_pointer(self) -> None:
        """Redraw the pointer to the correct position"""

        #Reference the rect obj selected
        pointed_obj = self.rects[self.selected]

        #Create the pointer object
        self.pointer = ImageObject(pointed_obj.left - 40, pointed_obj.center[1], 40, 30, self.sprites['pointer'], self.debug)

        #Draw the pointer on the screen
        self.pointer.draw(self.screen)

    def write_lines(self) -> None:
        """Write lines for the menu"""

        #Draw the title
        self.write(self.title_font, WHITE, "Space Invaders", self.screen_width//2, self.screen_height//5)

        #Draw the Play button
        self.rect_play = self.write(self.end_font,WHITE, "Play", self.screen_width//2, self.screen_height//2)

        #Draw the highscore button
        self.rect_highscore = self.write(self.end_font, WHITE, "High Score", self.screen_width//2, self.screen_height//15 + self.screen_height//2)

        #Draw the instructions button
        self.rect_instruction = self.write(self.end_font, WHITE, "Instructions", self.screen_width//2, self.screen_height//7.5 + self.screen_height//2)

        #Draw the settings button
        self.rect_settings = self.write(self.end_font, WHITE, "Settings", self.screen_width//2, self.screen_height//5 + self.screen_height//2)

        #Draw the quit button
        self.rect_end = self.write(self.end_font, WHITE, "Quit", self.screen_width//2, self.screen_height//1.2)

    def update_keypresses(self) -> State:
        """Track the keypress for the menu"""

        #Get the keypresses of the user
        keys = pygame.key.get_pressed()

        #Check if the user press the return key
        if keys[K_RETURN]:

            #Start the game
            return self.effects[self.selected]

        #If selector is moved down
        if (keys[K_s] or keys[K_DOWN]) and not self.pointer_cd:

            #Refresh pointer cd
            self.pointer_cd = 15

            #Move the selected down
            self.selected = (self.selected + 1) % len(self.rects)

        #If selector is moved up
        if (keys[K_w] or keys[K_UP]) and not self.pointer_cd:

            #Refresh pointer cd
            self.pointer_cd = 15

            #Move the selected up
            self.selected = (self.selected - 1) % len(self.rects)

        #If the pointer is on cooldown
        if self.pointer_cd:

            #Reduce its cooldown
            self.pointer_cd -= 1

    def handle(self) -> State:
        """Load the Menu onto the screen"""
        #Update the screen
        self.update()

        #Check for keypress of user
        state = self.update_keypresses()

        #Update the selector
        self.refresh_pointer()

        #Check the position of the mouse to return the state and combine it with the keypress of user
        return state if state else self.check_mouse(self.rects, self.effects)
