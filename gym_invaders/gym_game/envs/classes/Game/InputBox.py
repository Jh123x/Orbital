import pygame
from pygame.locals import *
try:
    from .Colors import *
except ImportError:
    from Colors import *

class InputBox(object):
    def __init__(self, initial_x:int, initial_y:int, height:int, font, max_length:int = 10):
        """Constructor for the inputbox
            Arguments:
                initial_x: Initial x position (int)
                initial_y: Initial y position (int)
                height: Height of the input box (int)
                font: Font of the box (pygame.Font)
                max_length: Maximum length of the input (int): default = 10
            
            Methods:
                update: Update the rect of the Inputbox
                clear: Clear the contents of the inputbox
                add: Add a char to the inputbox input
                blit: Draw the inputbox onto the screen
                backspace: Remove the last char that was entered
                get_text: Get the text in the inputbox

        """

        #Store the variables
        self.text = []
        self.max_length = max_length
        self.x = initial_x
        self.y = initial_y
        self.height = height
        self.color = WHITE
        self.font = font

        #Update the rect of the inputBox
        self.update()

    def update(self) -> None:
        """Update the InputBox
            Arguments:
                No arguments
            Returns: 
                No return
        """
        self.width = len(self.text)*15
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.center = (self.x, self.y)
    
    def clear(self) -> None:
        """Clear the input
            Arguments:
                No arguments
            Returns: 
                No return
        """
        self.text.clear()

    def add(self, char:str) -> None:
        """Add input
            Arguments:
                char: Input to be added (str)
            Returns: 
                No return
        """
        if char and len(self.text) <= self.max_length:
            self.text.append(char.strip())

    def blit(self, screen) -> None:
        """Draw the inputbox onto the screen
            Arguments:
                Screen: Screen that the box is rendered onto (pygame.Surface)
            Returns: 
                No return
        """
        screen.blit(self.font.render(self.get_text(), True, WHITE), self.rect)

    def backspace(self) -> None:
        """Remove the last letter
            Arguments:
                No arguments
            Returns: 
                No return
        """
        #If the text is not empty
        if self.text:
            #Remove the last character
            self.text.pop()

    def get_text(self) -> str:
        """Get what is in the inputbox
            Arguments:
                No arguments
            Returns: 
                Returns the string that was inputted
        """
        return "".join(self.text)
        
def main():
    """Main function used for debugging"""

    #Initialise the font and pygame
    pygame.init()
    pygame.font.init()

    #Set the display
    screen = pygame.display.set_mode((100,100))

    #Draw the box
    box = InputBox(50,50,50,pygame.font.Font(pygame.font.get_default_font(),15))

    #Game loop
    while True:

        #Keep track of the keys
        for event in tuple(filter(lambda x: x.type==pygame.KEYDOWN, pygame.event.get())):
            if event.key == K_BACKSPACE:
                print("Backspace")
                box.backspace()
            elif event.key != K_RETURN:
                print(event.unicode)
                box.add(event.unicode)
            else:
                print("Return")
                return

        #Update the image
        box.update()

        #Draw it onto the screen
        box.blit(screen)

        #Print what is the input currently
        print(box.get_text())


#If the file is run as main run the main function
if __name__ == '__main__':
    main()


