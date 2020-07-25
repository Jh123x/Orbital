from . import StoryTemplate, Screen
from .. import State, ImageObject, Direction, WHITE, Brute

class Stage4Screen(StoryTemplate):

    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, debug:bool):
        """The constructor for the Stage 3 screen"""

        #Call the superclass init method
        super().__init__(screen_width, screen_height, screen, State(103), sensitivity, max_fps, 1, debug)

        #Commander brief image
        self.bg = ImageObject(300, 285, 600, 570, StoryTemplate.sprites[0], debug)

        #Image of figure head (To be replaced with the actual image)
        self.alon_dusk = ImageObject(300, 215, 217, 217, StoryTemplate.sprites[2], debug)
        self.alon_dusk.scale(217,217)

        #Textbox
        self.tb = ImageObject(300, 685, 600, 230, StoryTemplate.sprites[6], debug)

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

            #Increment the clicks
            self.clicks += 1

            #Reset the cooldown
            self.click_cd = self.fps//5

        #Write the character name text
        self.write_main(Screen.end_font, WHITE, "Alon Dusk ", 33, self.tb.rect.top + 15, Direction.LEFT)

        #Pixel vars for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        if self.clicks == 0:

            #Write the character speech text
            self.render_speech(first_px, left_px, ["Commander, Mars is in peril. After a long and hard struggle,",
                                                "our people are starting to lose hope. "])

        elif self.clicks == 1:

            #Write part 2 of the speech 
            self.render_speech(first_px, left_px, ["We need you to stop their elite Bruiser units from ",
                                                "penetrating our defenses."])

        elif self.clicks == 2:

            #Write part 3 of speech
            self.render_speech(first_px, left_px, ["They form a hive mind, and every time one is defeated,",
                                                    "they adapt and grow stronger in response."])

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            self.next_scene()

        #Return the current state
        return self.state

    def post_cutscene(self):
        """The post cutscene for stage 3"""
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

            #Increment the clicks
            self.clicks += 1

            #Reset the cooldown
            self.click_cd = self.fps//5

        #Write the character name text
        self.write_main(Screen.end_font, WHITE, "Alon Dusk", 33, self.tb.rect.top + 15, Direction.LEFT)

        #Pixels for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        #Drawing of the speech
        if self.clicks == 0:

            #Write the character speech text
            self.render_speech(first_px, left_px, ["The enemy’s main forces are ahead in the Asteroid Belt."])

        elif self.clicks == 1:

            #Write part 2 of speech
            self.render_speech(first_px, left_px, ["Commander, we will need your help now more than ever",
                                                "to strike the decisive blow."])

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            self.next_scene()

            #Move to the next scene
            return self.get_victory_state()

        #Return the current state
        return self.state

    def spawn_scout(self):
        """Do not spawn scouts"""
        return

    def _spawn_brute(self, x):
        """Spawn a brute at position X, Y"""

        #Fix brute health at 3
        Brute.spawn_count = 3

        #Add a brute to the enemies group
        self.other_enemies.add(Brute(self.sensitivity, x, self.screen_height//10, self.screen_width, self.screen_height, self.mob_bullet, self.debug))

    def spawn_brute(self):
        """Spawn brutes"""

        #If it is the last wave
        if self.wave == 8:
            
            #Spawn 3 brutes
            for i in range(1, 4):
                self._spawn_brute(self.screen_width // 4 * i)

        #If it is the last 3 waves except last wave
        elif self.wave > 4:

            #Spawn 2 brute
            self._spawn_brute(self.screen_width // 2)

    def play(self):
        """The playing stage for the game"""

        #Call the superclass play
        return super().play()

    def win_condition(self):
        """The win condition of the player"""
        return self.wave == 9