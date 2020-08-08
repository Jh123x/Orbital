from . import StoryTemplate
from .. import State, ImageObject, Direction, WHITE, Scout, StatTracker

class Stage3Screen(StoryTemplate):

    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, tracker:StatTracker,debug:bool):
        """The constructor for the Stage 3 screen"""

        #Call the superclass init method
        super().__init__(screen_width, screen_height, screen, State(102), sensitivity, max_fps, 0.1,tracker,debug)

        #Commander brief image
        self.bg = ImageObject(self.screen_width//2, int(self.screen_height * 285 / 800), 600, 570, StoryTemplate.sprites_dict["commander_brief"], debug)
        self.bg.scale(self.screen_width, int(self.screen_height * 57/80))

        #Image of figure head
        self.marco = ImageObject(self.screen_width//2, int(self.screen_height * 210 / 800), 217, 217, StoryTemplate.sprites_dict['yuckerberg'], debug)
        self.marco.scale(int(217 * screen_width//600),int(217 * screen_height//800))

        #Image of the commander
        self.commander = ImageObject(self.screen_width//2, int(self.screen_height * 210 / 800), 217, 217, StoryTemplate.sprites_dict['silloette_commander'], debug)
        self.commander.scale(int(217 * screen_width//600), int(217 * screen_height//800))

        #Textbox
        self.tb = ImageObject(self.screen_width//2, int(self.screen_height * 685 / 800), 600, 230, StoryTemplate.sprites_dict['textbox'], debug)
        self.tb.scale(self.screen_width, int(self.screen_height * 23/80))

    def draw_bg(self):
        """Draw the background"""
        #Draw the commander brief
        self.bg.draw(self.screen)

        #Draw the textbox
        self.tb.draw(self.screen)

    def pre_cutscene(self):
        """The pre_cutscene for the class"""

        #Insert the Icon for the char speaking
        self.marco.draw(self.screen)

        #Draw the background
        self.draw_bg()

        #Draw the next button
        self.next_btn = self.write_main(self.end_font, WHITE, "Next", (580/600 * self.screen_width), self.tb.rect.top - 30, Direction.RIGHT)

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
        self.write_main(self.end_font, WHITE, "Marco Yuckerberg", 33, self.tb.rect.top + 15, Direction.LEFT)

        #Pixel vars for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        if self.clicks == 0:

            #Write the character speech text
            self.render_speech(first_px, left_px, ["Commander, Venus is a key industrial base and data center",
                                                "for us to collect data on the alien threat."])

        elif self.clicks == 1:

            #Write part 2 of the speech 
            self.render_speech(first_px, left_px, ["Enemy scouts of the main force have arrived and can fatally",
                                                "damage our defensive line. ",
                                                "We need you to preemptively strike down the enemies and",
                                                "stop their advance."])

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            self.next_scene()

        #Return the current state
        return self.state

    def post_cutscene(self):
        """The post cutscene for stage 3"""
        
        #Lower cd of click if it is still on cooldown
        if self.click_cd:
            self.click_cd -= 1

        #Check if the next button is clicked
        if self.check_clicked(self.next_btn) and not self.click_cd:

            #Increment the clicks
            self.clicks += 1

            #Reset the cooldown
            self.click_cd = self.fps//5
        
        #Insert the Icon for the char speaking
        if self.clicks <= 0:
            self.marco.draw(self.screen)
        else:
            self.commander.draw(self.screen)

        #Draw the background
        self.draw_bg()

        #Draw the next button
        self.next_btn = self.write_main(self.end_font, WHITE, "Next", (580/600 * self.screen_width), self.tb.rect.top - 30, Direction.RIGHT)

        #Pixels for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        #Drawing of the speech
        if self.clicks == 0:

            #Write the character name text
            self.write_main(self.end_font, WHITE, "Marco Yuckerberg", 33, self.tb.rect.top + 15, Direction.LEFT)

            #Write the character speech text
            self.render_speech(first_px, left_px, ["We have successfully prevented their vanguard from arriving,",
                                                "but our brethren on Mars are reporting that the aliens are",
                                                "ravaging their lands."])

        elif self.clicks == 1:

            #Write the character name text
            self.write_main(self.end_font, WHITE, "Commander", 33, self.tb.rect.top + 15, Direction.LEFT)

            #Write the character speech text
            self.render_speech(first_px, left_px, ["Mars… the first colony, and the reason for that war in ",
                                                    "the first place."])

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            self.next_scene()

            #Move to the next scene
            return self.get_victory_state()

        #Return the current state
        return self.state

    def _spawn_scout(self, x, y):
        """Spawn a scout at position x and y"""
        #Add the scout to the other enemies grp
        self.other_enemies.add(Scout(self.sensitivity, x, y, 1,  self.screen_width, self.screen_height, self.mob_bullet, self.debug))

    def spawn_scout(self):
        """Set the condition for scout to spawn"""

        #If wave 2
        if self.wave == 2:
            
            #Spawn 1 scout
            self._spawn_scout(self.screen_width // 2, self.screen_height // 10)

        #If wave 5
        elif self.wave == 5:

            #Spawn 2 scout
            self._spawn_scout(self.screen_width // 3, self.screen_height // 10)
            self._spawn_scout(self.screen_width // (3/2), self.screen_height // 10)

        #If wave 7
        elif self.wave == 7:

            #Spawn 3 scout
            self._spawn_scout(self.screen_width // 4, self.screen_height // 10)
            self._spawn_scout(self.screen_width // 2, self.screen_height // 10)
            self._spawn_scout(self.screen_width // (4/3), self.screen_height // 10)


    def play(self):
        """The playing stage for the game"""

        #Call the superclass play
        return super().play()

    def win_condition(self):
        """The win condition of the player"""
        return self.wave == 8