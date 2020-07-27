from . import StoryTemplate
from .. import State, ImageObject, Direction, WHITE

class Stage2Screen(StoryTemplate):

    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, debug:bool):
        """The constructor for the Stage 2 screen"""

        #Call the superclass init method
        super().__init__(screen_width, screen_height, screen, State(101), sensitivity, max_fps, 0.1, debug)

        #Commander brief image
        self.bg = ImageObject(300, 285, 600, 570, StoryTemplate.sprites['commander_brief'], debug)

        #Image of figure head
        self.tonald_drump = ImageObject(300, 215, 217, 217, StoryTemplate.sprites['drump'], debug)
        self.tonald_drump.scale(217,217)

        #Textbox
        self.tb = ImageObject(300, 685, 600, 230, StoryTemplate.sprites['textbox'], debug)

    def draw_bg(self):
        """Draw the background"""
        #Draw the commander brief
        self.bg.draw(self.screen)

        #Draw the textbox
        self.tb.draw(self.screen)

    def pre_cutscene(self):
        """The pre_cutscene for the class"""

        #Insert the Icon for the char speaking
        self.tonald_drump.draw(self.screen)

        #Draw the background
        self.draw_bg()

        #Draw the next button
        self.next_btn = self.write_main(self.end_font, WHITE, "Next", 580, self.tb.rect.top - 30, Direction.RIGHT)

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
        self.write_main(self.end_font, WHITE, "Tonald Drump", 33, self.tb.rect.top + 15, Direction.LEFT)

        #Pixel vars for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        if self.clicks == 0:

            #Write the character speech text
            self.render_speech(first_px, left_px, ["Our Moon Base, Elysium is under siege and in dire need of relief.",
                                                "The moon base is humanity’s first step to launch the counter",
                                                "offensive against the alien forces. "])

        elif self.clicks == 1:

            #Write part 2 of the speech 
            self.render_speech(first_px, left_px, ["Elysium is behind you with our full support to bomb them out of ",
                                                "our skies.",
                                                "They will be met with fire and fury and power the likes of which",
                                                "has not been seen before.",
                                                "And we will make humanity great again !"])

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            self.next_scene()

        #Return the current state
        return self.state

    def post_cutscene(self):
        """The post cutscene for stage 2"""
        #Insert the Icon for the char speaking
        self.tonald_drump.draw(self.screen)

        #Draw the background
        self.draw_bg()

        #Draw the next button
        self.next_btn = self.write_main(self.end_font, WHITE, "Next", 580, self.tb.rect.top - 30, Direction.RIGHT)

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
        self.write_main(self.end_font, WHITE, "Tonald Drump", 33, self.tb.rect.top + 15, Direction.LEFT)

        #Pixels for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        #Drawing of the speech
        if self.clicks == 0:

            #Write the character speech text
            self.render_speech(first_px, left_px, ["With Elysium relieved we can now strike back at the invaders",
                                                "much more effectively than before."])

        elif self.clicks == 1:

            #Write part 2 of the speech 
            self.render_speech(first_px, left_px, ["Strangely, these aliens seem to be following some",
                                                "kind of encrypted signal…"])

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            self.next_scene()

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
        return self.wave == 5
