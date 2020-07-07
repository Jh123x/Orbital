from .. import Colors, State
from . import Screen, Cutscene


class StoryModeScreen(Screen):
    videos = []
    def __init__(self, screen_width:int, screen_height:int, screen, initial_x:int, initial_y:int, debug:bool = False):
        """Constructor for Story mode screen"""

        #Call the superclass
        super().__init__(screen_width, screen_height, State.STORY_MENU, screen, 0, 0, debug)

        #Draw the title
        self.write(Screen.end_font, Color.WHITE, "Story modes", self.screen_width /2, self.screen_height /5)

        #Store the current number of stages
        self.stages = 1

        #Put a video for the StoryMode:
        self.create_videos()

    def get_stages(self) -> int:
        """Get the total number of stages in the story mode"""
        return self.stages

    def create_videos(self) -> None:
        """Create videos buttons for the videos"""

        #Create list to store the buttons
        self.video_buttons = []

        #Iterate through all the stage videos
        for i in range(1,self.get_stages()+1):

            #Append the button to the buttons list for checking later
            self.video_buttons.append(self.write(Screen.end_font, Color.WHITE, f"Stage {i}", self.screen_width /2, self.screen_height /2 + 20*i))

    def handle(self) -> None:
        """Call the superclass handle"""
        return super().handle()


