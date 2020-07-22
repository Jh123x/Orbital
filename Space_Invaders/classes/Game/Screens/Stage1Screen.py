from . import StoryTemplate, Screen
from .. import State, ImageObject, Direction, WHITE

class Stage1Screen(StoryTemplate):

    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, debug:bool):
        """The constructor for the Stage 1 screen"""

        #Call the superclass init method
        super().__init__(screen_width, screen_height, screen, State(100), sensitivity, max_fps, 0, debug)

        #Commander brief image
        self.bg = ImageObject(300, 285, 600, 570, StoryTemplate.sprites[0], debug)

        #Image of figure head
        self.alon_dusk = ImageObject(300, 200, 320, 320, StoryTemplate.sprites[2], debug)
        self.alon_dusk.scale(200,200)

        #Textbox
        self.tb = ImageObject(300, 685, 600, 230, StoryTemplate.sprites[3], debug)

    def reset(self) -> None:
        """Reset method for the stage class"""

        #Set the number of clicks to 0
        self.clicks = 0

        #Set the cooldown to max
        self.click_cd = self.fps // 5

        #Call the superclass reset
        return super().reset()

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

        #Draw the next button
        self.next_btn = self.write_main(Screen.end_font, WHITE, "Next", 580, self.tb.rect.top - 30, Direction.RIGHT)

        #Lower cd of click if it is still on cooldown
        if self.click_cd:
            self.click_cd -= 1

        #Check if the next button is clicked
        if self.check_clicked(self.next_btn) and not self.click_cd:
            if self.debug:
                print("Pressed next")
            self.clicks += 1
            self.click_cd = self.fps//5

        #Write the character name text
        self.write_main(Screen.end_font, WHITE, "Alon Dusk", 33, self.tb.rect.top + 15, Direction.LEFT)

        first_px = self.tb.rect.top + 75
        left_px = 40

        if self.clicks == 0:

            #Write the character speech text
            self.write_main(Screen.font, WHITE, "The enemy is at our doorstep, and we are in dire straits.", left_px, first_px, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "The enemy vanguard has surrounded Earth and is threatening", left_px, first_px + 15, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "our very survival", left_px, first_px + 30, Direction.LEFT)

        elif self.clicks == 1:

            #Write part 2 of the speech 
            self.write_main(Screen.font, WHITE, "We need you to break through their encirclement and", left_px, first_px, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "relieve earth from a land invasion.", left_px, first_px + 15, Direction.LEFT)

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            self.next_scene()

        #Return the current state
        return self.state

    def post_cutscene(self):
        """The post cutscene for stage 1"""
        self.next_scene()
        return self.state

    def play(self):
        """The playing stage for the game"""
        return super().play()

    def win_condition(self):
        """The win condition of the player"""
        return self.wave == 5
        