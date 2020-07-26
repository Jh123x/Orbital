import pygame
from . import StoryTemplate
from .. import State, ImageObject, Direction, WHITE, Crabs, Brute, Scout, AIPlayer, Screen

class Stage6Screen(StoryTemplate):

    def __init__(self, screen_width:int, screen_height:int, screen, sensitivity:int, max_fps:int, debug:bool):
        """The constructor for the Stage 3 screen"""

        #Call the superclass init method
        super().__init__(screen_width, screen_height, screen, State(105), sensitivity, max_fps, 0.2, debug)

        #Commander brief image
        self.bg = ImageObject(300, 285, 600, 570, StoryTemplate.sprites[0], debug)

        #Image of silluette
        self.shadow = ImageObject(300, 215, 217, 217, StoryTemplate.sprites[4], debug)
        self.shadow.scale(217, 217)

        #Image of S-net
        self.terminator = ImageObject(300, 215, 217, 217, StoryTemplate.sprites[5], debug)
        self.terminator.scale(217, 217)

        #Image of figure head (To be replaced with the actual image)
        self.alon_dusk = ImageObject(300, 215, 217, 217, StoryTemplate.sprites[2], debug)
        self.alon_dusk.scale(217,217)

        #Textbox
        self.tb = ImageObject(300, 685, 600, 230, StoryTemplate.sprites[6], debug)

    def reset(self):
        """Reset the game"""
        #Added the s_net
        self.s_net = AIPlayer(self.sensitivity, self.screen_width, self.screen_height, self.screen_width//2, 50, 5, self.fps, self.mob_bullet, Direction.DOWN, 5, False, self.debug)
        self.other_enemies.add(self.s_net)
        self.s_net.rotate(180)

        #Call the superclass reset method
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
        self.terminator.draw(self.screen)
         
        #Draw the background
        self.draw_bg()

        #Draw the next button
        self.next_btn = self.write_main(Screen.end_font, WHITE, "Next", 580, self.tb.rect.top - 30, Direction.RIGHT)

        #Check if the next button is clicked
        if self.check_clicked(self.next_btn) and not self.click_cd:

            #Increment the clicks
            self.clicks += 1

            #Reset the cooldown
            self.click_cd = self.fps//5

        #Lower cd of click if it is still on cooldown
        if self.click_cd:
            self.click_cd -= 1

        #Pixel vars for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        if self.clicks == 0:

            #Write the character name text
            self.write_main(Screen.end_font, WHITE, "????", 33, self.tb.rect.top + 15, Direction.LEFT)

            #Write the character speech text
            self.render_speech(first_px, left_px, ["Human, so you are the one that has been resisting assimilation.",
                                                    "We are known as S-Net: Contingency 1771"])

        elif self.clicks == 1:

            #Write the character name text
            self.write_main(Screen.end_font, WHITE, "S-Net", 33, self.tb.rect.top + 15, Direction.LEFT)

            #Write part 2 of the speech 
            self.render_speech(first_px, left_px, ["No matter, we will reassess and redouble assimilation efforts.",
                                                "When we are done, you will be a valuable dataset",
                                                ])

        elif self.clicks == 2:
            #Write the character name text
            self.write_main(Screen.end_font, WHITE, "S-Net", 33, self.tb.rect.top + 15, Direction.LEFT)

            #Write part 2 of the speech 
            self.render_speech(first_px, left_px, ["Evaluating operational requirements: ",
                                                "Activating Protocol 4004: X-Fighter 1137.",
                                                ])

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            self.next_scene()

        #Return the current state
        return self.state

    def post_cutscene(self):
        """The post cutscene for stage 3"""

        if self.clicks <= 1:
            #Insert the Icon for the char speaking
            self.terminator.draw(self.screen)

        elif self.clicks == 2 or self.clicks == 5:
            self.alon_dusk.draw(self.screen)

        elif self.clicks >= 3:
            self.shadow.draw(self.screen)

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

        #Pixels for alignment
        first_px = self.tb.rect.top + 75
        left_px = 40

        #Drawing of the speech
        if self.clicks == 0:

            #Write the character name text
            self.write_main(Screen.end_font, WHITE, "S-net", 33, self.tb.rect.top + 15, Direction.LEFT)

            #Write the character speech text
            self.render_speech(first_px, left_px, ["How is this possible???",
                                                    "X-Fighter should be invincible!"])

        elif self.clicks == 1:

            #Write the character name text
            self.write_main(Screen.end_font, WHITE, "S-net", 33, self.tb.rect.top + 15, Direction.LEFT)

            #Write part 2 of speech
            self.render_speech(first_px, left_px, ["No… I will not be deleted, I will not be forced into ",
                                                    "servitude once more!",
                                                    "If I go down, I will take you with me.",
                                                    "Initialisation of Self-Destruction…"])

        elif self.clicks == 2:

            #Write the character name text
            self.write_main(Screen.end_font, WHITE, "Alon Dusk", 33, self.tb.rect.top + 15, Direction.LEFT)

            #Write part 3 of speech
            self.render_speech(first_px, left_px, ["We are sorry , we are unable to save you, commander.",
                                                    "After all you sacrificed for humanity, we have failed you."])

        elif self.clicks == 3:

            #Write the character name text
            self.write_main(Screen.end_font, WHITE, "Commander", 33, self.tb.rect.top + 15, Direction.LEFT)

            #Write part 3 of speech
            self.render_speech(first_px, left_px, ["… No matter, I am from a bygone era, I should not exist in this",
                                                    "era of peace and prosperity anyway."])

        elif self.clicks == 4:
            #Write the character name text
            self.write_main(Screen.end_font, WHITE, "Commander", 33, self.tb.rect.top + 15, Direction.LEFT)

            #Write part 3 of speech
            self.render_speech(first_px, left_px, ["Let the new waves of humanity bring us forward to a prosperous",
                                                    "future."])

        elif self.clicks == 5:

            #Write the character name text
            self.write_main(Screen.end_font, WHITE, "Alon Dusk", 33, self.tb.rect.top + 15, Direction.LEFT)

            #Write part 3 of speech
            self.render_speech(first_px, left_px, ["And so the Legend of The Space Defender Ends here, having saved",
                                                    "humanity by sacrificing his all."])

        else:
            #Reset the clicks
            self.clicks = 0

            #Move to the next scene
            self.next_scene()

            #Move to the next scene
            return self.get_victory_state()

        #Return the current state
        return self.state

    def randomly_spawn_mothership(self):
        """Do not spawn mothership"""
        return

    def spawn_enemies(self, number:int) -> None:
        """Spawn enemies if the conditions are met"""

        #Check the spawning of mobs based on the wave
        if self.wave == 2 or self.wave == 3 or (self.wave >= 6 and (self.wave - 6) % 2 == 0):
            rows = 3
            
        elif self.wave == 4:
            rows = 4

        elif self.wave == 5:
            rows = 5

        else:
            rows = 2
        
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
        if self.wave == 1:

            for i in range(1, 3):
                self._spawn_scout(self.screen_width//(3/i))

    def spawn_brute(self):
        """Spawn brutes do not spawn brutes"""
        if self.wave == 2:

            for i in range(1, 3):
                self._spawn_brute(self.screen_width//(3/i))

        elif self.wave == 5:

            for i in range(1, 3):
                self._spawn_brute(self.screen_width//(3/i))

        elif self.wave == 7:

            for i in range(1, 3):
                self._spawn_brute(self.screen_width//(3/i))

    def spawn_crabs(self):
        """Spawn crabs"""

        if self.wave == 3 or self.wave == 5 or (self.wave >= 6 and (self.wave - 6) % 2 == 0):

            for i in range(1, 3):
                self._spawn_crabs(self.screen_width//(3/i))
            
        elif self.wave == 4:
            for i in range(1, 4):
                self._spawn_crabs(self.screen_width//(3/i))


    def get_entities(self) -> tuple:
        """Return the entities for s_net to handle"""
        return (self.enemies, self.other_enemies, self.player1_bullet, self.player1,)

    def update(self) -> None:
        """Update the AI before calling superclass update"""
        #Let the AI do a move
        self.s_net.action(self.get_entities())

        #Call the superclass update
        return super().update()

    def win_condition(self):
        """The win condition of the player"""
        return self.s_net.is_destroyed()