from . import Screen
from .. import State, WHITE, Direction, Sound, Background, Difficulty, GREY

class SettingsScreen(Screen):
    def __init__(self, screen_width:int, screen_height:int, screen, fps:int, sound:Sound, background:Background, difficulty: Difficulty, volume:float, debug:bool = False):
        """Constructor for the settings screen"""

        #Call the superclass
        super().__init__(screen_width, screen_height, State.SETTINGS, screen, 0, 0, debug = debug)

        #Store the variables
        self.fps = fps
        self.sound = sound
        self.bg = background
        self.difficulty = difficulty

        #Set a cooldown
        self.cooldown = self.fps//10

        #Draw the Header
        self.write(self.title_font, WHITE, "Settings", screen_width//2, screen_height//5)

        #Draw the back button
        self.back = self.write(self.end_font, WHITE, "Back", screen_width//2, screen_height//1.2)

    def get_bg_no(self) -> int:
        """Get the current background that the user chose"""
        return self.bg.get_bg_no()

    def get_music_enabled(self) -> bool:
        """Get the state of music"""
        return self.sound.get_state()

    def get_difficulty(self) -> str:
        """Get the difficulty name"""
        return self.difficulty.name

    def get_difficulty_no(self) -> int:
        """Get the difficulty number"""
        return self.difficulty.value

    def get_volume(self) -> float:
        """Return the volume of the sound"""
        return self.sound.get_volume()

    def handle_mouse_presses(self) -> State:
        """Handle the mouse presses on the settings screen"""

        #Set click initially to be false
        clicked = False

        #If it is not on cooldown
        if self.cooldown <= 0:

            #If the back button is clicked
            if self.check_clicked(self.back):
                
                #Go back to the screen
                return State.MENU

            #If the background button is pressed
            elif self.check_clicked(self.background):

                #Cycle the background
                self.bg.cycle()
                clicked = True

            #If the music button is pressed
            elif self.check_clicked(self.music):

                #Toggle the music state
                self.sound.toggle()
                clicked = True

            #If the difficulty button is pressed
            elif self.check_clicked(self.difficulty_rect):

                #Toggle difficulty
                self.difficulty.toggle()
                clicked = True

            #Check if the sound button is pressed
            elif self.check_clicked(self.sound_btn) and self.get_music_enabled():

                #Toggle the sound
                self.sound.volume_toggle()
                clicked = True
                
        #If the user clicked
        if clicked:

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
        self.background = self.write_main(self.end_font, WHITE, f"Background: {self.get_bg_no()}", self.screen_width//4, first_pixel, Direction.LEFT)
        self.music = self.write_main(self.end_font, WHITE, f"Music: {'On' if self.get_music_enabled() else 'Off'}", self.screen_width//4, first_pixel + self.screen_height//15, Direction.LEFT)
        self.difficulty_rect = self.write_main(self.end_font, WHITE, f"Difficulty: {self.get_difficulty().title()}", self.screen_width//4, first_pixel + self.screen_height//7.5, Direction.LEFT)

        #If sound is enabled
        if self.get_music_enabled():

            #Write to the screen that the music is enabled
            self.sound_btn = self.write_main(self.end_font, WHITE, f"Sound: {int(self.get_volume()*100)}", self.screen_width//4, first_pixel + self.screen_height//5, Direction.LEFT)

        #Otherwise
        else:

            #Write that the music is disabled
            self.sound_btn = self.write_main(self.end_font, GREY, f"Sound: {int(self.get_volume()*100)}", self.screen_width//4, first_pixel + self.screen_height//5, Direction.LEFT)

        #Return based on what the user press
        return self.handle_mouse_presses()