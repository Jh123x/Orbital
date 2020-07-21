from . import StoryTemplate
from .. import State, ImageObject

class Stage1Screen(StoryTemplate):

    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, debug:bool):
        """The constructor for the Stage 1 screen"""

        #Call the superclass init method
        super().__init__(screen_width, screen_height, screen, State(100), sensitivity, max_fps, debug)

        #Commander brief image
        self.bg = ImageObject(300, 285, 600, 570, StoryTemplate.sprites[0], debug)

        #Image of figure head
        self.alon_dusk = ImageObject(300, 200, 320, 320, StoryTemplate.sprites[2], debug)
        self.alon_dusk.scale(200,200)

        #Textbox
        self.tb = ImageObject(300, 685, 600, 230, StoryTemplate.sprites[3], debug)

    def draw_bg(self):
        """Draw the background"""
        #Draw the commander brief
        self.bg.draw(self.screen)

        #Draw the textbox
        self.tb.draw(self.screen)

    def pre_cutscene(self):
        """The pre_cutscene for the class"""

        #Insert the Icon for the char speaking
        self.alon_dusk.draw(self.screen)

        #Draw the background
        self.draw_bg()

        #Write the text
        # self.write_main(self)

        return self.state

    def post_cutscene(self):
        """The post cutscene for stage 1"""
        return self.get_victory_state()

    def play(self):
        """The playing stage for the game"""
        return super().play()

    def win_condition(self):
        """The win condition of the player"""
        return self.wave == 5
        