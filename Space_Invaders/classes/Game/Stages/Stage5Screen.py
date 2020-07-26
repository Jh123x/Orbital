from . import StoryTemplate
from .. import State, ImageObject, Direction, WHITE, Crabs, Brute, Scout, Screen

class Stage5Screen(StoryTemplate):

    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, debug:bool):
        """The constructor for the Stage 3 screen"""

        #Call the superclass init method
        super().__init__(screen_width, screen_height, screen, State(104), sensitivity, max_fps, 0.2, debug)

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
        self.write_main(Screen.end_font, WHITE, "Alon Dusk", 33, self.tb.rect.top + 15, Direction.LEFT)

        #Pixel vars for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        if self.clicks == 0:

            #Write the character speech text
            self.render_speech(first_px, left_px, ["The main forces of the enemy are here, and they have strange tricks",
                                                "up their sleeves."])

        elif self.clicks == 1:

            #Write part 2 of the speech 
            self.render_speech(first_px, left_px, ["Be wary of the CRABS who attack in unorthodox ways,",
                                                "and break our formations. We must break through with ",
                                                "a full frontal assault!"])

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
            self.render_speech(first_px, left_px, ["Strange, results of the analysis of the enemy have come back,",
                                                    "and it appears that they all come from a common source in Pluto."])

        elif self.clicks == 1:

            #Write part 2 of speech
            self.render_speech(first_px, left_px, ["This means that the threat… is not from an alien at all! ",])

        elif self.clicks == 2:
            #Write part 3 of speech
            self.render_speech(first_px, left_px, ["It points towards instead that something in Pluto is manufacturing",
                                                    "these Invading Creatures and sending them against us."])

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            self.next_scene()

            #Move to the next scene
            return self.get_victory_state()

        #Return the current state
        return self.state

    def spawn_enemies(self, number:int) -> None:
        """Spawn enemies if the conditions are met"""

        #Check the spawning of mobs based on the wave
        if self.wave == 1:
            rows = 2

        elif self.wave >= 2 and self.wave < 5:
            rows = 3
            
        elif self.wave == 5:
            rows = 1
        
        elif self.wave >= 6 and self.wave < 8:
            rows = 4

        else:
            row = 5

        return super().spawn_enemies(rows*6)

    def _spawn_brute(self, x):
        """Spawn a brute at position X, Y"""

        #Add a brute to the enemies group
        self.other_enemies.add(Brute(self.sensitivity, x, self.screen_height//10, self.screen_width, self.screen_height, self.mob_bullet, self.debug))

    def _spawn_scout(self, x):
        """Spawn a scout at position x and y"""
        #Add the scout to the other enemies grp
        self.other_enemies.add(Scout(self.sensitivity, x, self.screen_height//10, 1,  self.screen_width, self.screen_height, self.mob_bullet, self.debug))

    def _spawn_crabs(self, x):
        #Add the scout to the other enemies grp
        self.other_enemies.add(Crabs(self.sensitivity, x, self.screen_height//10, 1,  self.screen_width, self.screen_height, self.mob_bullet, self.debug))

    def spawn_scout(self):
        """Spawn scouts"""

        #Spawn scouts for the appropriate wave
        if self.wave == 3:
            self._spawn_scout(self.screen_width//2)

        elif self.wave >= 7:

            for i in range(1, 3):
                self._spawn_scout(self.screen_width//(3/i))

    def spawn_brute(self):
        """Spawn brutes do not spawn brutes"""
        if self.wave == 2:
            self._spawn_brute(self.screen_width//2)

        elif self.wave == 5:

            for i in range(1, 3):
                self._spawn_brute(self.screen_width//(3/i))

    def spawn_crabs(self):
        """Spawn crabs"""        
        if self.wave == 4:

            self._spawn_crabs(self.screen_width//3)
            self._spawn_crabs(self.screen_width//(3/2))

        elif self.wave == 5 or self.wave == 6:

            for i in range(1, 5):
                self._spawn_crabs(self.screen_width//(4/i))

        elif self.wave == 8:
            for i in range(1, 9):
                self._spawn_crabs(self.screen_width//(8/i))

    def play(self):
        """The playing stage for the game"""

        #Call the superclass play
        return super().play()

    def win_condition(self):
        """The win condition of the player"""
        return self.wave == 9