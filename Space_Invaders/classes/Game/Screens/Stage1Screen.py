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
        self.dill_bates = ImageObject(300, 210, 320, 320, StoryTemplate.sprites[3], debug)
        self.dill_bates.scale(217,217)

        #Textbox
        self.tb = ImageObject(300, 685, 600, 230, StoryTemplate.sprites[5], debug)

    def draw_bg(self):
        """Draw the background"""
        #Draw the commander brief
        self.bg.draw(self.screen)

        #Draw the textbox
        self.tb.draw(self.screen)

    def pre_cutscene(self):
        """The pre_cutscene for the class"""

        #Insert the Icon for the char speaking
        self.dill_bates.draw(self.screen)

        #Draw the background
        self.draw_bg()

        #Draw the next button
        self.next_btn = self.write_main(Screen.end_font, WHITE, "Next", 580, self.tb.rect.top - 30, Direction.RIGHT)

        #Lower cd of click if it is still on cooldown
        if self.click_cd:
            self.click_cd -= 1

        #Check if the next button is clicked
        if self.check_clicked(self.next_btn) and not self.click_cd:

            #Increment the clicks
            self.clicks += 1

            #Reset the cooldown
            self.click_cd = self.fps//5

        #Write the character name text
        self.write_main(Screen.end_font, WHITE, "Dill Bates", 33, self.tb.rect.top + 15, Direction.LEFT)

        #Pixel vars for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        if self.clicks == 0:

            #Write the character speech text
            self.write_main(Screen.font, WHITE, "Commander, the enemy is at our doorstep, and we are in dire straits,", left_px, first_px, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "the enemy has surrounded Earth and is threatening our very survival", left_px, first_px + 15, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "The enemies here are the cannon fodder of their invasion.", left_px, first_px + 30, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "However we cannot underestimate their strength.", left_px, first_px + 45, Direction.LEFT)

        elif self.clicks == 1:

            #Write part 2 of the speech 
            self.write_main(Screen.font, WHITE, "The enemies here are the cannon fodder of their invasion. ", left_px, first_px, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "However we cannot underestimate their strength.", left_px, first_px + 15, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "As we are unable to access our main weapon caches ", left_px, first_px + 30, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "on our Moon Base either...", left_px, first_px + 45, Direction.LEFT)

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            self.next_scene()

        #Return the current state
        return self.state

    def post_cutscene(self):
        """The post cutscene for stage 1"""
        #Insert the Icon for the char speaking
        self.dill_bates.draw(self.screen)

        #Draw the background
        self.draw_bg()

        #Draw the next button
        self.next_btn = self.write_main(Screen.end_font, WHITE, "Next", 580, self.tb.rect.top - 30, Direction.RIGHT)

        #Lower cd of click if it is still on cooldown
        if self.click_cd:
            self.click_cd -= 1

        #Check if the next button is clicked
        if self.check_clicked(self.next_btn) and not self.click_cd:

            #Increment the clicks
            self.clicks += 1

            #Reset the cooldown
            self.click_cd = self.fps//5

        #Write the character name text
        self.write_main(Screen.end_font, WHITE, "Dill Bates", 33, self.tb.rect.top + 15, Direction.LEFT)

        #Pixels for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        if self.clicks == 0:

            #Write the character speech text
            self.write_main(Screen.font, WHITE, "Good job clearing the way. Now we can prepare to", left_px, first_px, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "take our Moon Base. ", left_px, first_px + 15, Direction.LEFT)

        elif self.clicks == 1:

            #Write the character speech text
            self.write_main(Screen.font, WHITE, "However, there is something weird about the remains", left_px, first_px, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "of these invaders.", left_px, first_px + 15, Direction.LEFT)

        elif self.clicks == 2:

            #Write the character speech text
            self.write_main(Screen.font, WHITE, "They seem to be made of some kind of biochemical alloy", left_px, first_px, Direction.LEFT)
            self.write_main(Screen.font, WHITE, "we had been researching on Pluto...", left_px, first_px + 15, Direction.LEFT)

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            return self.get_victory_state()

        #Return the current state
        return self.state

    def play(self):
        """The playing stage for the game"""

        #Call the superclass play
        return super().play()

    def win_condition(self):
        """The win condition of the player"""
        return self.wave == 4
        