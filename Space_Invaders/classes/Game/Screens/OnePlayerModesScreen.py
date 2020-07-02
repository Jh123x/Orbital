from . import Screen
from .. import State, WHITE

class OnePlayerModeScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """The main screen for 1 player mode"""

        #Call the superclass
        super().__init__(screen_width, screen_height, State.ONE_PLAYER_MENU, screen, 0, 0, debug)

        #Single player modes
        self.write(Screen.title_font, WHITE, "1 Player modes", screen_width//2, screen_height//5)

        #Draw the screen for the story mode
        storymode = self.write(Screen.end_font, WHITE, "Story Mode", screen_width//2, screen_height//2)

        #Draw the rectangles for the classic button
        classic = self.write(Screen.end_font, WHITE, "Classic Mode", screen_width//2, screen_height//15 + screen_height//2)

        #Draw the rectangles for the endless button
        endless = self.write(Screen.end_font, WHITE, "Endless Mode", screen_width//2, screen_height//7.5 + screen_height//2)

        #Draw the online button
        online = self.write(Screen.end_font, WHITE, "Online Mode", screen_width//2, screen_height//5 + screen_height//2)

        #Draw the back button
        back = self.write(Screen.end_font, WHITE, "Back", screen_width//2, screen_height//1.2)

        #Store the button rects
        self.buttons = [storymode, classic, endless, online, back]
        self.modes = [State.STORY_MENU, State.CLASSIC, State.PLAY, State.ONLINE, State.PLAYMODE]

    def check_keypresses(self) -> State:
        """Check keypresses of the user"""

        #Check if any buttons were clicked
        result = tuple(map(lambda x: self.check_clicked(x), self.buttons))

        #Iterate through the clicks
        for index, click in enumerate(result):

            #If anything was clicked
            if click:

                #Return the corresponding mode
                return self.modes[index]

        #Otherwise return current state
        return self.state

    def handle(self) -> State:
        """Handle the drawing of the one player mode screen"""

        #Call the superclass handle
        super().update()

        #Check keypresses of the user
        return self.check_keypresses()

