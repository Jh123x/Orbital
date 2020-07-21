from .. import WHITE, State
from . import Screen

class StoryModeScreen(Screen):
    videos = []
    def __init__(self, screen_width:int, screen_height:int, screen, debug:bool = False):
        """Constructor for Story mode screen"""

        #Call the superclass
        super().__init__(screen_width, screen_height, State.STORY_MENU, screen, 0, 0, debug)

        #Draw the title
        self.write(Screen.title_font, WHITE, "Story modes", self.screen_width /2, self.screen_height /5)

        #Store the current number of stages
        self.stages = 1

        #Create list to store the buttons
        self.video_buttons = []

        #Put a video for the StoryMode:
        self.create_videos()

        #Draw the back button
        self.back = self.write(Screen.end_font, WHITE, "Back", self.screen_width // 2, self.screen_height / 1.2)

    def get_stages(self) -> int:
        """Get the total number of stages in the story mode"""
        return self.stages

    def create_videos(self) -> None:
        """Create videos buttons for the videos"""

        #Iterate through all the stage videos
        for i in range(1,self.get_stages()+1):

            #Append the button to the buttons list for checking later
            self.video_buttons.append(self.write(Screen.end_font, WHITE, f"Stage {i}", self.screen_width // 2, self.screen_height //2 + (40*i)))

    def check_mousepress(self) -> State:
        """Check the mouse press of the user"""
        #Check if the user clicked the back button
        if self.check_clicked(self.back):

            #Return menu state
            return State.ONE_PLAYER_MENU

        #Loop through the the video buttons
        for index,rect in enumerate(self.video_buttons):
            if self.check_clicked(rect):
                return State(100 + index)

        return self.state

    def handle(self) -> None:
        """Handle the drawing of the screen"""

        #Call the superclass update
        super().update()

        #Check mousepress of user
        return self.check_mousepress()


