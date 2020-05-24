import pygame
try:
    from .Screens import Screen
    from .Colors import WHITE
    from .Enums import State, Direction
    from .Object import Object
except ImportError:
    from Screens import Screen
    from Colors import WHITE
    from Enums import State
    from Object import Object

class Popup(Screen):
    def __init__(self, popup_width:int, popup_height:int, sentence:str, tick_life:int, initial_x:int, initial_y:int, screen, debug:bool = False):
        """Main Popup class"""
        self.ttl = tick_life
        self.sentence = sentence

        #Call the Screen superclass init
        super().__init__(popup_width, popup_height, State.NONE, screen, initial_x - (len(sentence) * 5), initial_y, debug)

        #Fill itself black
        self.set_background((0,0,0))

        #Render the words for the popup
        self.write(Screen.font, WHITE, sentence, initial_x - len(sentence) * 14, initial_y)

    def update(self):
        """Update function for the popup"""
        #Reduce the ttl of the popup
        if self.ttl:
            self.ttl -= 1
            super().update()
            return self
        else:
            return None


if __name__ == '__main__':
    #Initialise pygame
    pygame.init()
    pygame.font.init()

    #Vars
    screen_width = 600
    screen_height = 800
    fps = 60

    #Init screen
    screen = pygame.display.set_mode((screen_width, screen_height))

    #Set fps
    clock = pygame.time.Clock()

    #Create popup obj
    popup = Popup(100,100,"Test", 500, 0, 0, screen)

    while running:

        #Clock the fps
        clock.tick(fps)

        #Fill background with black
        screen.fill((0,0,0))

        #Draw the popup
        popup.update()

        #Update the display with the screen
        pygame.display.update()

        #If the state is quit or player closes the game
        if pygame.QUIT in tuple(map(lambda x: x.type, pygame.event.get())):
            running = False