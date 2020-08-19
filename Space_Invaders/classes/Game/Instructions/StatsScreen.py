from .. import State, WHITE, MenuTemplate

class StatsScreen(MenuTemplate):
    def __init__(self, screen_width:int, screen_height:int, screen, stat_tracker, debug:bool = False):
        """Screen the shows the player's stats"""

        #Store the stat tracker
        self.stat_tracker = stat_tracker
        
        #Call the superclass
        super().__init__(screen_width, screen_height, State.STAT_MENU, screen, 0, debug)

    def write_lines(self) -> None:
        """Override the method in the subclass"""

        #Write the header
        self.write(self.title_font, WHITE, "Statistics", self.screen_width // 2, self.screen_height//5)
        
        #Write the main words
        self.write_main_words()
        
        #Write the back line
        self.back = self.write(self.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height//1.2)

    def write_main_words(self):
        #Get items
        lines = self.stat_tracker.get_all()

        #Draw the lines based on the stat tracker
        for index,(header,stat) in enumerate(lines):

            #Write the stat
            self.write_main(self.h2_font, WHITE, f"{header}: {stat}", self.screen_width //2 , self.screen_height // 2 - 100 + 25 * index)

    def get_rects(self) -> None:
        """Rects on the screen"""
        return [self.back]

    def get_effects(self) -> None:
        """Effects of the rects"""
        return [State.MENU]

    def handle(self) -> State:
        """Handle the drawing of the settings screen"""

        #Write the main words
        self.write_main_words()

        #Call the superclass handle
        return super().handle()


