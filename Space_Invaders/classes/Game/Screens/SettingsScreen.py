from . import MenuTemplate
from .. import State, WHITE, Direction, Sound, Background, Difficulty, GREY

class SettingsScreen(MenuTemplate):
    def __init__(self, screen_width:int, screen_height:int, screen, fps:int, sound:Sound, background:Background, difficulty: Difficulty, volume:float, debug:bool = False):
        """Constructor for the settings screen"""
        #Store the variables
        self.fps = fps
        self.sound = sound
        self.bgr = background
        self.difficulty = difficulty

        #Call the superclass
        super().__init__(screen_width, screen_height, State.SETTINGS, screen, debug)

    def write_lines(self) -> None:
        """Write the lines for the settings screen"""

        #Draw the Header
        self.write(self.title_font, WHITE, "Settings", self.screen_width//2, self.screen_height//5)

        #Draw the back button
        self.back = self.write(self.end_font, WHITE, "Back", self.screen_width//2, self.screen_height//1.2)

        #Write the updated stats
        self.write_main_words()

    def write_main_words(self) -> None:
        """Write the main lines"""

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

    def get_rects(self):
        """Return the rects of the rect"""
        return (self.background, self.music, self.difficulty_rect, self.sound_btn, self.back)

    def get_effects(self):
        """Return the effects for the rects"""
        return (self.cycle_background, self.toggle_sound, self.toggle_difficulty, self.toggle_volume, State.MENU)

    def get_bg_no(self) -> int:
        """Get the current background that the user chose"""
        return self.bgr.get_bg_no()

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

    def cycle_background(self) -> State:
        """Cycle the background"""
        self.bgr.cycle()
        return self.state

    def toggle_sound(self) -> State:
        """Toggle the sound"""
        self.sound.toggle()
        return self.state
    
    def toggle_difficulty(self) -> State:
        self.difficulty.toggle()
        return self.state

    def toggle_volume(self) -> State:
        self.sound.volume_toggle()
        return self.state

    def handle(self) -> State:
        """Handle the drawing of the settings screen"""

        #Write the main words
        self.write_main_words()

        #Call the superclass handle
        return super().handle()