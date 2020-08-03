import pygame
from pygame.locals import *
from . import Screen
from .. import State, WHITE, ImageObject

class MenuTemplate(Screen):

    def __init__(self, screen_width:int, screen_height:int, state: State, screen, curr_pointer:int = 0, debug:bool = False):
        """Constructor for the menu template"""
        #Call the superclass
        super().__init__(screen_width, screen_height, state, screen, 0, 0, debug)

        #Preprocess items
        self.preprocess()

        #Write the lines required for the Menu
        self.write_lines()

        #Store the rects and the effects
        self.rects = self.get_rects()
        self.effects = self.get_effects()

        #Store the current pointer
        self.curr_pointer = curr_pointer

        #Reset the menu
        self.reset()

    def write_lines(self) -> None:
        """Override the method in the subclass"""
        raise NotImplementedError("Please Implement the write_lines method in your class")

    def get_rects(self) -> None:
        """Override the method in the subclass"""
        raise NotImplementedError("Please Implement get_rects method in the class")

    def get_effects(self) -> None:
        """Override the method in the subclass"""
        raise NotImplementedError("Please Implement get_effects method in the class")

    def preprocess(self) -> None:
        """Override the method in the subclass to add items to preprocessing"""
        pass

    def check_mouse(self, rects:list, states:list):
        """Check the position of the mouse on the menu to see what the player clicked"""
        
        #Iterate through each of the rects
        for i in range(len(rects)):

            #Check if the rect is clicked
            if self.check_clicked(rects[i]) and not self.pointer_cd:
                
                #Reset pointer cd
                self.pointer_cd = 20

                #Return the state if it is clicked
                if type(states[i]) == State:
                    return states[i]
                else:
                    return states[i]()

        #Otherwise return the Menu state
        return self.state

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
        self.pointer = ImageObject(pointed_obj.left - 40, pointed_obj.center[1], 40, 30, self.pointers[self.curr_pointer], self.debug)

        #Draw the pointer on the screen
        self.pointer.draw(self.screen)

    def update_keypresses(self) -> State:
        """Track the keypress for the menu"""

        #Get the keypresses of the user
        keys = pygame.key.get_pressed()

        #Check if the user press the return key
        if keys[K_RETURN] and not self.pointer_cd:

            #Store selected index
            pt = self.selected

            #Refresh pointer cd
            self.pointer_cd = 15

            #If it is a state
            if type(self.effects[pt]) == State:

                #Reset the pointer if it mutates the state
                self.reset()

                #Return the State
                return self.effects[pt]

            else:
                #Otherwise call the function
                return self.effects[pt]()


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

        #Update the selector
        self.refresh_pointer()

        #Check for keypress of user
        state = self.update_keypresses()

        #Check the position of the mouse to return the state and combine it with the keypress of user
        return state if state else self.check_mouse(self.rects, self.effects)