from . import Screen, Popup
from .. import State, WHITE, Direction, Sound, Background

class SettingsScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, fps:int, sound:Sound, background:Background, debug:bool = False):
        """Constructor for the settings screen"""

        #Call the superclass
        super().__init__(screen_width, screen_height, State.SETTINGS, screen, 0, 0, debug = debug)

        #Store the variables
        self.fps = fps
        self.sound = sound

        #Music 
        self.bg = background

        #Set a cooldown
        self.cooldown = self.fps//10

        #Draw the Header
        self.write(Screen.title_font, WHITE, "Settings", screen_width//2, screen_height//5)

        #Draw the back button
        self.back = self.write(Screen.end_font, WHITE, "Back", screen_width//2, screen_height//1.2)

    def get_bg_no(self) -> int:
        """Get the current background that the user chose"""
        return self.bg.get_bg_no()

    def get_music_enabled(self) -> bool:
        """Get the state of music"""
        return self.sound.get_state()

    def handle_mouse_presses(self) -> State:
        """Handle the mouse presses on the settings screen"""

        #If it is not on cooldown
        if self.cooldown <= 0:

            #If the back button is clicked
            if self.check_clicked(self.back):
                return State.MENU

            #If the background button is pressed
            if self.check_clicked(self.background):
                self.bg.cycle()

                #Reset the cooldown
                self.cooldown = self.fps//10

            #If the music button is pressed
            if self.check_clicked(self.music):

                #Toggle the music state
                self.sound.toggle()

                #Reset the cooldown
                self.cooldown = self.fps//10
        
        #Otherwise
        else:
            if self.debug:
                print(f"On cooldown: {self.cooldown}")

            #Reduce the cooldown
            self.cooldown -= 1

        #Return the current state
        return self.state

    def handle(self) -> State:
        """Handle the drawing of the settings screen"""
        #Update the screen
        self.update()

        #First pixel used for alignment
        first_pixel = self.screen_height//2

        #Draw the different settings options
        self.background = self.write_main(Screen.end_font, WHITE, f"Background: {self.get_bg_no()}", self.screen_width//4, first_pixel, Direction.LEFT)
        self.music = self.write_main(Screen.end_font, WHITE, f"Music enabled: {self.get_music_enabled()}", self.screen_width//4, first_pixel + self.screen_height//15, Direction.LEFT)

        #Return based on what the user press
        return self.handle_mouse_presses()


